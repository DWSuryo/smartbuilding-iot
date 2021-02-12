import os

class Config:
    #import secrets --> secrets.token_hex(16)
    SECRET_KEY = 'bb8660b6e81499a8bf47b75844cc8afc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')