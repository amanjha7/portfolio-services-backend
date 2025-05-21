from flask import Flask
from flask_cors import CORS
from app.extensions import mongo
from app.extensions import mail
from app.routes import api
from config import Config

def create_app():
    app = Flask(__name__)

    # ── Make sure the URI names a database:
    app.config["MONGO_URI"] = (
        "mongodb+srv://aman:aman"
        "@mediaplayercluster.ggsfnxd.mongodb.net/"
        "myportfolio"
        "?retryWrites=true&w=majority&appName=mediaPlayerCluster"
    )

    app.config["MAIL_SERVER"]= Config.MAIL_SERVER
    app.config["MAIL_PORT"] = Config.MAIL_PORT  
    app.config["MAIL_USE_TLS"] = Config.MAIL_USE_TLS
    app.config["MAIL_USERNAME"] = Config.MAIL_USERNAME
    app.config["MAIL_PASSWORD"] = Config.MAIL_PASSWORD
    app.config["MAIL_DEFAULT_SENDER"] = Config.MAIL_DEFAULT_SENDER

    # This binds mongo.db → your database
    mongo.init_app(app)
    mail.init_app(app)

    CORS(app)
    app.register_blueprint(api, url_prefix="/api")
    return app
