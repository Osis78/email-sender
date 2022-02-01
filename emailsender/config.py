from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOADS_FOLDER = 'uploads/'

# create and configure the app
app = Flask(__name__)
app.secret_key = b'639dbfd0c1460947b1c1bdf178dfef9d1de468620b16c8842aa210edc3e2cfee'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emailsender.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
