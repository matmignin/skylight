#!/usr/bin/env python3

import os
from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.debug = True
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
# app.config['MAIL_USE_TLS'] = 1
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = 'mathough2@gmail.com'
# app.config['MAIL_PASSWORD'] = 
# app.config['MAIL_DEFAULT_SENDER'] = 'mathough2@gmail.com'


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "kilgore"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "pdf"}
app.config["UPLOAD_FOLDER"] = os.path.join(
    # os.path.dirname(os.path.abspath(__file__)), "static/uploads/"
    os.path.abspath(os.path.dirname(__file__)), "static/uploads/"
)
# toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from webapp import routes
