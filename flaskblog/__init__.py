from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flask_socketio import SocketIO
import eventlet
import os.path
from whitenoise import WhiteNoise

eventlet.monkey_patch()
socketio = SocketIO()   #updated
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_iew = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = WhiteNoise(app.wsgi_app)
    my_static_folders = (
        'static/'
        'static/profile_pics/',
        'static/tab/',
    )
    for static in my_static_folders:
        app.wsgi_app.add_files(static)

    # if os.path.isfile('site.db'):
    #     print ("site.db exist")
    # else:
    #     db.create_all()

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.cam.routes import cam
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(cam)

    socketio.init_app(app, ping_interval=5, ping_timeout=10) #updated for socket
    return app