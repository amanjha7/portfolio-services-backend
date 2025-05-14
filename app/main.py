from flask import Flask
from flask_cors import CORS
from app.extensions import mongo
from app.routes import api

def create_app():
    app = Flask(__name__)

    # ── Make sure the URI names a database:
    app.config["MONGO_URI"] = (
        "mongodb+srv://aman:aman"
        "@mediaplayercluster.ggsfnxd.mongodb.net/"
        "myportfolio"
        "?retryWrites=true&w=majority&appName=mediaPlayerCluster"
    )

    # This binds mongo.db → your database
    mongo.init_app(app)

    CORS(app)
    app.register_blueprint(api, url_prefix="/api")
    return app
