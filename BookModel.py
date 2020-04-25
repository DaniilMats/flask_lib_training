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
