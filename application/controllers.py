from flask import render_template, current_app as app

from models.models import Article, User, db
from flask import request
from flask_marshmallow import Marshmallow
from marshmallow import post_load

ma = Marshmallow(app)


class UserSchema(ma.Schema):
    class Meta:
        model = User
        fields = ("id", "username", "email")

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


userchema = UserSchema()
usersschema = UserSchema(many=True)


@app.route('/', methods=['GET'])
def index_get():
    return {"message": "success"}


@app.route('/users', methods=['POST'])
def users_post():
    rq = request.json
    new_user = userchema.load(rq)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "user_created"}, 201


@app.route('/users', methods=['GET'])
def users_get():
    users = User.query.all()
    return usersschema.dump(users), 200


@app.route('/articles', methods=['GET'])
def articles_get():
    articles = Article.query.all()
    for arti in articles:
        print(arti.title)
        print(arti.content)
    return render_template("articles.html")
