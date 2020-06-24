#!/usr/bin/env python3
from flask import (
    render_template,
    request,
    url_for,
    flash,
    redirect,
    session,
    send_from_directory,
)
import os
from webapp import app, db, bcrypt
from webapp.forms import RegisterForm, LoginForm
from webapp.models import User
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

upload_folder = app.config["UPLOAD_FOLDER"]


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        try:
            db.session.commit()
            flash(f"account created for {form.username.data}!", "success")
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("that username is already in use")
            return redirect(url_for('signup'))
    return render_template("signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('upload'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Youre logged in!", "success")
                files = os.listdir(upload_folder)
                return render_template("gallery.html", files=files)
            else:
                # db.session.rollback()
                flash("not a correct password")
                return redirect(url_for('signup'))
        else:
            flash("Thats not a user. Sign up")
            # return render_template("signup.html", form=user)
            return redirect(url_for('signup'))
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/gallery', methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        if request.files:
            input = request.files["inputFile"]
            if input.filename == "":
                flash("no file selected")
                return redirect(request.url)
            else:
                for upload in request.files.getlist("inputFile"):
                    upload.save(os.path.join(upload_folder, upload.filename))
    files = os.listdir(upload_folder)
    return render_template("gallery.html", files=files)


@app.route("/gallery/<filename>")
@login_required
def send_image(filename):
    return send_from_directory(upload_folder, filename)
