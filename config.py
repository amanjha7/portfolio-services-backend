import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'amanjhavdjs12tha@gmail.com'  # ✅ Correct this
    MAIL_PASSWORD = 'jsig wppi nlsg awrv'         # ✅ Your app password
    MAIL_DEFAULT_SENDER = 'amanjhavdjs12tha@gmail.com'

