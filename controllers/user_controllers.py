import datetime

import jwt
from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import config
from models.models import User

from serializers.user_serializers import user_signup_schema, user_display_schema, users_display_schema

db = SQLAlchemy()

user_controller = Blueprint('user_controller', __name__, url_prefix='/api/users')


@user_controller.route("/signup", methods=["POST"])
def api_user_signup():
    try:
        user_from_request = request.json
        user = user_signup_schema.load(user_from_request)
        if user:
            hashed_password = generate_password_hash(user.password, method="sha256")
            user.password = hashed_password
            db.session.add(user)
            db.session.commit()
            token = jwt.encode(
                {"user_id": user.id,
                 "username": user.username,
                 "email": user.email,
                 "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)},
                config.secret_key
            )
            return {"user": user_display_schema.dump(user), "token": token}
    except ValidationError:
        return jsonify({"message": "bad_request"}), 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "internal_server_error"}), 500


@user_controller.route('/', methods=["GET"])
def api_users_get():
    try:
        users = User.query.all()
        return users_display_schema.dump(users), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "error"}), 500


@user_controller.route('/login', methods=["POST"])
def api_user_login():
    try:
        body_data = request.get_json()
        if body_data["email"] and body_data["password"]:
            email_from_request = body_data["email"]
            password_from_request = body_data["password"]
            user = User.query.filter(User.email == email_from_request).first()
            if user and check_password_hash(user.password, password_from_request):
                token = jwt.encode(
                    {"user_id": user.id,
                     "username": user.username,
                     "email": user.email,
                     "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)},
                    config.secret_key
                )
                return jsonify({"user": user_display_schema.dump(user), "token": token}), 200
            return {"message": "invalid_credentials"}, 401
        return {"message": "invalid_data"}, 400
    except Exception as e:
        print("Exception", e)
        return jsonify({"message": "internal_server_error"}), 500
