#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length
from webapp.models import User, FileContents
from webapp import db


class LoginForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")
