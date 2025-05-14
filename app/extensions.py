from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_pymongo import PyMongo

mongo = PyMongo()


db = SQLAlchemy()
ma = Marshmallow()
