import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


path = os.path.dirname(os.path.abspath(__file__))
dbPath = os.path.join(path, 'test.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisIsSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbPath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
