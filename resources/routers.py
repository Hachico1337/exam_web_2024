from flask_restful import Resource
from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.models import *
from schemas.sheme import *
from utils.save_image import *

# везде где id - это id книги

class Books(Resource):
    def get(self):
        """
        список книг на главной странице
        """
        data = execute_data("""
            SELECT 
                books.id AS book_id, 
                books.name AS name, 
                books.year, 
                GROUP_CONCAT(DISTINCT genres.name) AS genres, 
                AVG(reviews.rating) as avg_rating, 
                COUNT(DISTINCT reviews.id) AS count_reviews
            FROM books
            LEFT JOIN book_to_genres ON books.id = book_to_genres.book_id
            LEFT JOIN genres ON book_to_genres.genre_id = genres.id
            LEFT JOIN reviews ON reviews.book_id = books.id
            GROUP BY books.id
            ORDER BY books.year DESC;
        """)
        return BooksSchema(many=True).dump(data), 200

    @jwt_required()
    def post(self):
        """
        создание новой книги
        """
        name = request.form.get('name')
        description = request.form.get('description')
        year = int(request.form.get('year'))
        publisher = request.form.get('publisher')
        author = request.form.get('author')
        pages = int(request.form.get('pages'))
        genres = request.form.getlist('genres')
        # получаем и сохраняем изображение
        img = request.files.get('image')
        filename = img.filename
        file_data = img.read()
        md5_hash = hash_file(file_data)
        cover = Cover.find_by_hash(md5_hash)
        if not cover:
            cover = Cover(filename, img.mimetype, md5_hash)
            cover.save()
            type = cover.mime_type.split("/")
            save_image(f'{cover.id}.{type[1]}', file_data)
        # сохраняем данные
        book = Book(name, description, year, publisher, author, pages, cover.id)
        book.save()
        for i in genres:
            book_to_genre(book.id, int(i)).save()
        return make_response(jsonify({'message': 'success'}), 200)


class WorkBook(Resource):
    @jwt_required()
    def get(self, id):
        """
        получение инфы об одной книге
        """
        data = Book.query.get(id)
        book = BookSchema(many=False).dump(data)
        type = Cover.query.get(book['cover_id']).mime_type.split("/")
        book['cover'] = f'{request.host_url}/uploads/{book["cover_id"]}.{type[1]}'
        genres = execute_data(f"""
        SELECT group_concat(genres.name)
        from genres
        JOIN book_to_genres on book_to_genres.genre_id = genres.id
        where book_to_genres.book_id = {book['id']};
        """)
        book['genres'] = genres[0][0]
        return book

    @jwt_required()
    def put(self, id):
        """
        изменение книги
        """
        try:
            book = Book.query.get(id)
            if not book:
                return make_response(jsonify({'message': 'book not found'}), 404)
            name = request.form.get('name')
            description = request.form.get('description')
            year = int(request.form.get('year'))
            publisher = request.form.get('publisher')
            author = request.form.get('author')
            pages = int(request.form.get('pages'))
            book.name = name
            book.description = description
            book.year = year
            book.publisher = publisher
            book.author = author
            book.pages = pages
            return make_response(jsonify({'message': 'book updated'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    @jwt_required()
    def delete(self, id):
        """
        удаление книги и обложки
        """
        try:
            book = Book.query.get(id)
            if not book:
                return make_response(jsonify({'message': 'book not found'}), 404)
            cover = Cover.query.get(book.cover_id)
            type = cover.mime_type.split("/")
            os.remove(f'{os.getcwd()}/uploads/{cover.id}.{type[1]}')
            cover.delete()
            book.delete()
            return make_response(jsonify({'message': 'success'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': 'failed delete'}), 400)


class WriteReview(Resource):
    @jwt_required()
    def get(self, id):
        """
        получаем реценцию
        """
        review = Review.find_review(id, get_jwt_identity())
        if not review:
            return make_response(jsonify({'message': 'not found'}), 404)
        else:
            return ReviewSchema(many=False).dump(review), 200

    @jwt_required()
    def post(self, id):
        """
        создаем новую рецензию
        """
        try:
            rating = int(request.form.get('rating'))
            comment = request.form.get('comment')
            Review(id, get_jwt_identity(), rating, comment).save()
            return make_response(jsonify({'message': 'success'}), 200)
        except Exception as e:
            return make_response(jsonify({'error': e}))


class UserInfo(Resource):
    @jwt_required()
    def get(self):
        """
        получаем данные о пользователе
        """
        user_info = execute_data(f"""
        select users.surname, users.name, users.lastname, roles.name as role
        from users
        join roles on users.role_id = roles.id
        where users.id = {get_jwt_identity()}
        """)
        return UserSchema.schema_many(user_info), 200
