from flask_marshmallow import Marshmallow
from marshmallow import post_load

from models.models import User

ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_image", "admin")


class UserMinimalDisplaySchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "username", "email", "profile_image")


class UserDisplaySchema(ma.Schema):
    class Meta:
        model = User
        fields = (
            "id", "username", "email", "profile_image", "admin", "about", "time_created")


class UserSignupSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("username", "email", "password")

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


user_schema = UserSchema()
user_signup_schema = UserSignupSchema()
user_display_schema = UserDisplaySchema()
users_display_schema = UserDisplaySchema(many=True)
user_minimal_display_schema = UserMinimalDisplaySchema()
users_minimal_display_schema = UserMinimalDisplaySchema(many=True)
