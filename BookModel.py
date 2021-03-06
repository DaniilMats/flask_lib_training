from flask_sqlalchemy import SQLAlchemy
from settings import app
import json

db: SQLAlchemy = SQLAlchemy(app)


class Book(db.Model):
    """
    Класс создает таблицу books. И обеспечивает доступ к данным таблицы.
    """
    __tablename__: str = 'books'
    author = db.Column(db.String(80), nullable=False)
    book_name = db.Column(db.String(80), nullable=False)
    id = db.Column(db.Integer, primary_key=True)

    def add_book(book_info: dict):
        """
        Добавляет книгу в бд.
        """
        new_book: Book = Book(author=book_info.get('author'),
                              book_name=book_info.get('book_name'),
                              id=book_info.get('id'))
        db.session.add(new_book)
        db.session.commit()

    def json(self):
        """
        Обеспечивает валидный формат данных для json
        """
        return {'author': self.author, 'book_name': self.book_name, 'id': self.id}

    def get_all_books():
        """
        Достает все книги и добавляет их в список
        """
        return [Book.json(book) for book in Book.query.all()]

    def get_book_by_id(_id):
        """
        Достает книгу по id
        """
        return Book.query.filter_by(id=_id).first()

    def delete_book(_id):
        """
        Удаляет книгу по id
        """
        Book.query.filter_by(id=_id).delete()
        db.session.commit()

    def update_book(_id: int, book_info: dict):
        """
        Обновляет инфорамацию о книге по id
        """
        book_to_update: Book = Book.query.filter_by(id=_id).first()
        author_name: str = book_info.get('author')
        book_name: str = book_info.get('book_name')
        if author_name:
            book_to_update.author = author_name
        if book_name:
            book_to_update.book_name = book_name
        db.session.commit()

    def __repr__(self):
        """
        Отображение данных в терминале
        """
        book: dict = {
            'author': self.author,
            'book_name': self.book_name,
            'id': self.id
        }
        return json.dumps(book)


db.create_all()
