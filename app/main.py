from flask import Flask
from config import Config
from app.extensions import db, ma
from app.routes import api
from app.extensions import mongo
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    # app.config.from_object(Config)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/mymodernportfolio"
    mongo.init_app(app)

    # db.init_app(app)
    # ma.init_app(app)
    CORS(app)  # Enable CORS for all routes

    app.register_blueprint(api, url_prefix='/api')

    return app
