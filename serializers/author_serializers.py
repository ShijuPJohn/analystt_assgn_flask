from flask_marshmallow import Marshmallow
from marshmallow import post_load

from models.models import Author

ma = Marshmallow()


class AuthorSchema(ma.Schema):
    class Meta:
        model = Author
        fields = ("id", "name", "about")

    @post_load
    def make_author(self, data, **kwargs):
        return Author(**data)


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)
