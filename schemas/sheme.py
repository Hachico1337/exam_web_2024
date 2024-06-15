import flask_marshmallow as ma


class SchemaBase(ma.Schema):
    @classmethod
    def schema_many(cls, arg):
        if len(arg) > 1:
            return cls(many=True).dump(arg)
        else:
            return cls(many=False).dump(arg[0])


class UserSchema(SchemaBase, ma.Schema):
    class Meta:
        fields = ('surname', 'name', 'lastname', 'role')


class ReviewSchema(SchemaBase, ma.Schema):
    class Meta:
        fields = ('rating', 'comment', "date_created")


class BooksSchema(SchemaBase, ma.Schema):
    class Meta:
        fields = ('book_id', 'name', 'genres', 'year', 'avg_rating', 'count_reviews')


class BookSchema(SchemaBase, ma.Schema):
    class Meta:
        fields = ('id', 'description', 'year', 'publisher', 'author', 'pages',
                  'cover_id', 'cover', 'genres')
