from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import app
import json

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__: str = 'books'
    author = db.Column(db.String(80),  nullable=False)
    book_name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def add_book(_author, _book_name, _id):
        new_book = Book(author=_author, book_name=_book_name, id=_id)
        db.session.add(new_book)
        db.session.commit()

    def get_all_books():
        return Book.query.all()

    def get_book_by_id(_id):
        return Book.query.filter_by(id=_id).first()

    def __repr__(self):
        book: dict = {
            'author': self.author,
            'book_name': self.book_name,
            'id': self.id
        }
        return json.dumps(book)

