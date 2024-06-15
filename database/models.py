from flask_sqlalchemy import SQLAlchemy

from datetime import date

from sqlalchemy import text
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


def execute_data(query: str):
    result = db.session.execute(text(query))
    return result.fetchall()


class Base:
    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()


class Cover(db.Model, Base):
    __tablename__ = 'covers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    mime_type = db.Column(db.String(256), nullable=False)
    md5_hash = db.Column(db.String(256), nullable=False)

    def __init__(self, name: str, mime_type: str, md5_hash: str):
        self.name = name
        self.mime_type = mime_type
        self.md5_hash = md5_hash

    @classmethod
    def find_by_hash(cls, md5_hash: str) -> 'Cover':
        return cls.query.filter_by(md5_hash=md5_hash).first()


class Book(db.Model, Base):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    publisher = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    cover_id = db.Column(db.Integer, db.ForeignKey('covers.id', onupdate='CASCADE', ondelete='CASCADE'),
                         nullable=False)

    def __init__(self, name: str, description: str, year: int, publisher: str, author: str, pages: int, cover_id: int):
        self.name = name
        self.description = description
        self.year = year
        self.publisher = publisher
        self.author = author
        self.pages = pages
        self.cover_id = cover_id


class Genre(db.Model, Base):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False, unique=True)

    def __init__(self, name: str):
        self.name = name


class book_to_genre(db.Model, Base):
    """
    связь многие ко многим
    """
    __tablename__ = 'book_to_genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', onupdate='CASCADE',
                                                  ondelete='CASCADE'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id', onupdate='CASCADE',
                                                   ondelete='CASCADE'), nullable=False)

    def __init__(self, book_id: int, genre_id: int):
        self.book_id = book_id
        self.genre_id = genre_id


class Role(db.Model, Base):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256), nullable=False)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class Users(db.Model, Base):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(256), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    surname = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    lastname = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', onupdate='CASCADE',
                                                  ondelete='CASCADE'), nullable=False)

    def __init__(self, login: str, password: str, surname: str, name: str, last_name=None, role_id: int = None):
        self.login = login
        self.password_hash = generate_password_hash(password)
        self.surname = surname
        self.name = name
        self.lastname = last_name
        self.role_id = role_id

    @classmethod
    def find_by_login(cls, login: str) -> 'Users':
        return cls.query.filter_by(login=login).first()

    @classmethod
    def check_role_id(cls, user_id: int) -> int:
        return cls.query.filter_by(user_id=user_id).first().role_id


class Review(db.Model, Base):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', onupdate='CASCADE',
                                                  ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE',
                                                  ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.Date, nullable=False, default=date.today())

    def __init__(self, book_id: int, user_id: int, rating: int, comment: str):
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    @classmethod
    def find_review(cls, book_id: int, user_id: int) -> "Review":
        return cls.query.filter_by(book_id=book_id, user_id=user_id).first()
