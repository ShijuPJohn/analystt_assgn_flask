import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func

db = SQLAlchemy()

author_book = db.Table("author_books",
                       db.Column("user_id", db.Integer, db.ForeignKey("author.id")),
                       db.Column("book_id", db.Integer, db.ForeignKey("book.id"))
                       )

book_genres = db.Table("book_genres",
                       db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
                       db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"))
                       )


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, unique=True)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    books = db.relationship("Book", backref="added_by")
    about = db.Column(db.String, nullable=True, default='')

    def __str__(self):
        return "User object" + self.email


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, unique=True)
    about = db.Column(db.String, nullable=True, default='')

    def __str__(self):
        return "User object" + self.name


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    isbn = db.Column(db.String, nullable=True)
    number_of_pages = db.Column(db.Integer, nullable=True)
    edition = db.Column(db.Integer, nullable=True)
    published_year = db.Column(db.Integer, nullable=True)
    cover_image = db.Column(db.String, nullable=True)  # TODO default=?
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())
    time_updated = db.Column(DateTime(timezone=True), server_default=func.now(),
                             onupdate=func.current_timestamp())
    authors = db.relationship("Author", secondary=author_book, backref="books")
    posted_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    archived = db.Column(db.Boolean, default=False, nullable=False)
    draft = db.Column(db.Boolean, default=False, nullable=False)
    genres = db.relationship("Genre", secondary=book_genres, backref="books")

    def __str__(self):
        return "Post with title : " + self.title


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __str__(self):
        return "Category with name : " + self.name
