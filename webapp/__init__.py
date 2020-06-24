#!/usr/bin/env python3

import os
from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.debug = True
# app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'mat@mignin.com'
app.config['MAIL_PASSWORD'] = 'gKilgore7744'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "kilgore"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "pdf"}
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "static/uploads/"
)
# toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from webapp import routes
