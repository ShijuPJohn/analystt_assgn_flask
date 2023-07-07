from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from sqlalchemy import or_

from controllers.token_validator import validate_token
from models.models import Genre, Author, Book
from serializers.book_serializers import book_create_schema, book_schema, genre_schema, books_minimal_display_schema

db = SQLAlchemy()

book_controller = Blueprint('book_controller', __name__, url_prefix='/api/books')


@book_controller.route('/', methods=["GET"])
def books_get():
    books = Book.query
    if "search" in request.args:
        books = books.filter(or_(Book.title.like(f"%{request.args['search']}%"),
                                 Book.description.like(f"%{request.args['search']}%")))
    if "limit" in request.args:
        books = books.limit(request.args["limit"])
    if "offset" in request.args:
        books = books.offset(request.args["offset"])
    books = books.all()
    if len(books) == 0:
        return jsonify({"message": "no books found"}), 404
    return jsonify({"total_number_of_books": len(books), "books": books_minimal_display_schema.dump(books)})


@book_controller.route('/genre', methods=["POST"])
@validate_token
def author_post(user_from_token):
    try:
        genre_from_request = request.json
        genre = genre_schema.load(genre_from_request)
        db.session.add(genre)
        db.session.commit()
        return jsonify({"author": genre_schema.dump(genre)}), 201
    except ValidationError as v:
        print("Validation Exception", v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "internal_server_error"}), 500


@book_controller.route("/", methods=["POST"])
@validate_token
def api_post_create(user_from_token):
    try:
        request_data = request.json
        genres_from_request = request_data["genres"]
        authors_from_request = request_data["authors"]
        genres_list = Genre.query.filter(Genre.id.in_(genres_from_request)).all()
        authors_list = Author.query.filter(Author.id.in_(authors_from_request)).all()
        request_data["genres"] = genres_list
        request_data["authors"] = authors_list
        request_data["posted_by_id"] = user_from_token.id
        book_object_from_request = book_create_schema.load(request_data)
        local_object = db.session.merge(book_object_from_request)
        db.session.add(local_object)
        db.session.commit()
        if user_from_token.admin:
            return {"message": "approved", "post": book_schema.dump(local_object)}, 201
        return {"message": "approval_pending", "post": book_schema.dump(local_object)}, 201

    except ValidationError as v:
        print("Validation Errror", v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "error"}), 500
