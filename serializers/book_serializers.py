from flask_marshmallow import Marshmallow
from marshmallow import post_load
from marshmallow_sqlalchemy import fields

from models.models import Book, Genre
from serializers.author_serializers import author_schema, authors_schema
from serializers.user_serializers import user_display_schema, user_minimal_display_schema, users_minimal_display_schema

ma = Marshmallow()


class GenreSchema(ma.Schema):
    class Meta:
        model = Genre
        fields = ("id", "name")

    @post_load
    def make_genre(self, data, **kwargs):
        return Genre(**data)


genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


class BookSchema(ma.Schema):
    class Meta:
        model = Book
        fields = (
            "id", "title", "description", "publisher", "isbn", "number_of_pages", "edition", "published_year",
            "cover_image", "time_created", "archived",
            "draft", "genres",
            "authors", "added_by")

    authors = fields.Nested(authors_schema)
    genres = fields.Nested(genres_schema)
    added_by = fields.Nested(user_minimal_display_schema)


class BookCreateSchema(ma.Schema):
    class Meta:
        model = Book
        fields = (
            "title", "description", "publisher", "isbn", "number_of_pages", "edition", "published_year",
            "cover_image", "draft", "genres",
            "authors", "posted_by_id")

    @post_load
    def make_post(self, data, **kwargs):
        return Book(**data)


class BookDisplaySchema(ma.Schema):
    class Meta:
        model = Book
        fields = (
            "id", "title", "description", "publisher", "isbn", "number_of_pages", "edition", "published_year",
            "cover_image", "time_created", "archived",
            "draft", "genres",
            "authors", "added_by", "approved")

    authors = fields.Nested(users_minimal_display_schema)
    genres = fields.Nested(genres_schema)


class BookMinimalDisplaySchema(ma.Schema):
    class Meta:
        model = Book
        fields = (
            "id", "title", "description", "publisher", "isbn", "number_of_pages", "edition", "published_year",
            "cover_image", "genres",
            "authors")

    authors = fields.Nested(users_minimal_display_schema)
    genres = fields.Nested(genres_schema)


book_schema = BookSchema()
books_schema = BookSchema(many=True)
books_display_schema = BookDisplaySchema(many=True)
book_display_schema = BookDisplaySchema()
book_minimal_display_schema = BookMinimalDisplaySchema()
books_minimal_display_schema = BookMinimalDisplaySchema(many=True)

book_create_schema = BookCreateSchema()
