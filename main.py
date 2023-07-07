import os.path

from flask import Flask
from flask_cors import CORS

from config import ProductionConfig, LocalDevelopmentConfig, get_secret
from models.models import db
from controllers.book_controllers import book_controller
from controllers.user_controllers import user_controller
from controllers.author_controllers import author_controller


def create_app():
    app_var = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
        app_var.config.from_object(ProductionConfig)
    else:
        app_var.config.from_object(LocalDevelopmentConfig)
    db.init_app(app_var)
    app_var.app_context().push()
    return app_var


app = create_app()
app.register_blueprint(book_controller)
app.register_blueprint(user_controller)
app.register_blueprint(author_controller)
cors = CORS(app)
app.config['SECRET_KEY'] = get_secret()
app.config['CORS_HEADERS'] = 'Content-Type'
app.app_context().push()
db.create_all()

if __name__ == "__main__":
    app.run(port=8080)
