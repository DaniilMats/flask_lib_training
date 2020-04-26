from flask import Flask
import os

dir_path: str = os.path.dirname(os.path.realpath(__file__))+'/database.db'
app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dir_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

