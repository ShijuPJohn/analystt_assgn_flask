from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from controllers.token_validator import validate_token
from serializers.author_serializers import author_schema

db = SQLAlchemy()

author_controller = Blueprint('author_controller', __name__, url_prefix='/api/authors')


@author_controller.route('/', methods=["POST"])
@validate_token
def author_post(user_from_token):
    try:
        author_from_request = request.json
        author = author_schema.load(author_from_request)
        db.session.add(author)
        db.session.commit()
        return jsonify({"author": author_schema.dump(author)}), 201
    except ValidationError as v:
        print("Validation Exception", v)
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "internal_server_error"}), 500
