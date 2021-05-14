import os
import secrets
import configparser

class Config:
    conf = configparser.ConfigParser()
    conf.read("credential.ini")
    #import secrets --> secrets.token_hex(16)
    
    #SECRET_KEY = secrets.token_hex(16)
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = conf["Flask"]["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = conf["Flask"]["SQLALCHEMY_DATABASE_URI"]
    #SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') 
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')