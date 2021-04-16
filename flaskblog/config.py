import os
import secrets

class Config:
    #import secrets --> secrets.token_hex(16)
    
    #SECRET_KEY = secrets.token_hex(16)
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = '5da34e07ea6f3c2c10aaba508b262c95'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')