from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:/home/dan/PycharmProjects/flask_edu/library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
