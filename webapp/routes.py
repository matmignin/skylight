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
from webapp import app, db, bcrypt, mail
from webapp.forms import RegisterForm, LoginForm
from webapp.models import User
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from flask_mail import Message

upload_folder = app.config["UPLOAD_FOLDER"]
# mat_folder = os.path.join(app.config["UPLOAD_FOLDER"], "mat")
# mike_folder = os.path.join(app.config["UPLOAD_FOLDER"], "mike")

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
            flash("account created for {0}!".format(form.username.data), "success")
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
                flash("{0} is logged in!".format(user.username), "success")
                return redirect(url_for('upload'))
            else:
                flash("not a correct password")
                return redirect(url_for('signup'))
        else:
            flash("Thats not a user. Sign up")
            return redirect(url_for('signup'))
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload', methods=["GET", "POST"])
@login_required
def upload():
    user_folder = os.path.join(upload_folder, str(current_user.username))
    if request.method == "POST":
        if request.files:
            input = request.files["form_upload"]
            if input.filename == "":
                flash("no file selected")
                return redirect(request.url)

            else:
                for upload in request.files.getlist("form_upload"):
                    upload.save(os.path.join(user_folder, upload.filename))
                    flash("{0} uploaded".format(upload.filename)) 
                    # msg = Message('test subject', recipients=['mat@mignin.com'])
                    # with app.open_resource(os.path.join(user_folder, upload.filename)) as fp:
                        # msg.attach('{0}'.format(upload.filename), 'image/*', fp.read())
                        # mail.send(msg)
    files = os.listdir(user_folder)
    return render_template("upload.html", files=files)


@app.route('/gallery', methods=["GET", "POST"])
def get_gallery():
    mat_folder = os.path.join(app.config["UPLOAD_FOLDER"], "mat")
    mat_files = os.listdir(mat_folder)
    mike_folder = os.path.join(app.config["UPLOAD_FOLDER"], "mike")
    mike_files = os.listdir(mike_folder)
    tony_folder = os.path.join(app.config["UPLOAD_FOLDER"], "tony")
    tony_files = os.listdir(tony_folder)
    christie_folder = os.path.join(app.config["UPLOAD_FOLDER"], "christie")
    christie_files = os.listdir(christie_folder)
    return render_template("gallery.html", 
                           mat_files=mat_files,
                           mike_files=mike_files,
                           tony_files=tony_files,
                           christie_files=christie_files)




@app.route("/upload/mat/<filename>")
def mat_image(filename):
    mat_folder = os.path.join(app.config["UPLOAD_FOLDER"], "mat")
    # mat_files = os.listdir(mat_folder)
    return send_from_directory(mat_folder, filename)


@app.route("/upload/mike/<filename>")
def mike_image(filename):
    mike_folder = os.path.join(app.config["UPLOAD_FOLDER"], "mike")
    # mike_files = os.listdir(mike_folder)
    return send_from_directory(mike_folder, filename)


@app.route("/upload/tony/<filename>")
def tony_image(filename):
    tony_folder = os.path.join(app.config["UPLOAD_FOLDER"], "tony")
    # tony_files = os.listdir(tony_folder)
    return send_from_directory(tony_folder, filename)


@app.route("/upload/christie/<filename>")
def christie_image(filename):
    christie_folder = os.path.join(app.config["UPLOAD_FOLDER"], "christie")
    # christie_files = os.listdir(christie_folder)
    return send_from_directory(christie_folder, filename)


@app.route("/upload/<filename>")
def all_image(filename):
    # all_folder = app.config["UPLOAD_FOLDER"]
    # all_files = os.listdir(r)
    return send_from_directory(upload_folder, filename)
