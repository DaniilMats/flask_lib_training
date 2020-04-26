from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

dir_path: str = os.path.dirname(os.path.realpath(__file__))+'/database.db'
app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dir_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db: SQLAlchemy = SQLAlchemy(app)
db.create_all()

