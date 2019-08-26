import flask
from flask import render_template, request, jsonify, Response, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from app import app, database

from . import models

import re

@app.route('/index')
def index():
    return render_template("index.html")



@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    #print(request.form)
    if request.method == "POST":
        #print(request.form["email"], request.form["password"])
        current_user = models.User.get_user_by_email(request.form["email"])
        if current_user.verify_password(request.form["password"]):
            login_user(current_user)
            flash('logged in successfully', "success")
            return redirect(url_for("dropzoneupload"))
            #print(current_user)
        else:
            flash("failed", "info")

    return render_template("login.html")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # Here we use a class of some kind to represent and validate our
#     # client-side form data. For example, WTForms is a library that will
#     # handle this for us, and we use a custom LoginForm to validate.
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Login and validate the user.
#         # user should be an instance of your `User` class
#         login_user(user)
#
#         flask.flash('Logged in successfully.')
#
#         next = flask.request.args.get('next')
#         # is_safe_url should check if the url is safe for redirects.
#         # See http://flask.pocoo.org/snippets/62/ for an example.
#         # if not is_safe_url(next):
#         #     return flask.abort(400)
#
#         return flask.redirect(next or flask.url_for('index'))
#     return flask.render_template('login.html', form=form)
######

def verify(email, password, username):
    checkEmail = re.compile(r'^(\w+_?-?\.?\w*)@([\w+\.]+[a-zA-Z]+$)')
    return checkEmail.match(email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        existuser = models.User.get_user_by_email(request.form["email"])
        if existuser:
            flash("email has been used", "info")
        if verify(request.form["email"], request.form["password"], request.form["username"]):
            #print(request.form["email"], request.form["password"], request.form["username"])
            newuser = models.User(request.form["username"], request.form["password"], request.form["email"])
            newuser.save()
            flash("registered successfully", "success")
        else:
            #print("failed")
            flash("failed", "info")
    return render_template("register.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logged out succesfully", "info")
    return redirect(url_for("login"))
    #return render_template('logout.html', current_user=current_user)



###

# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     if request.method == 'POST' and 'photo' in request.files:
#         filename = models.Image.save(request.files['photo'], current_user.get_id())
#         print("uploading:",filename)
#     return render_template('upload.html')



@app.route('/uploadbydropzone', methods=['POST', 'GET'])
@login_required
def dropzoneupload():
    print(request.files, request.method)
    if request.method == 'POST':
        print("dropzoneupload:", request.files, request.method)
        print("dropzoneupload_files:",request.files.getlist("file[0]"))

        for fnumber, f in request.files.items():
            print(f)
            print("name:",f.filename)
            print("*"*10)
            models.Image.save(f, current_user.get_id())

    return render_template('dropzone.html')


@app.route('/image/<imgname>')
def return_img_stream(imgname):
    resp = Response(models.Image(models.Image.find_by_name(imgname).name).get_img(), mimetype="image/jpeg")
    return resp


@app.route('/image')
def get_images():
    data = models.Image.get_all()
    return jsonify(data)

@app.route('/image/delete/<imgname>', methods=['GET'])
def delete(imgname):
    img = models.Image.find_by_name(imgname)
    resp = img.delete()
    return 'delete'+img.name

@app.route('/image/updatename/<imgname>', methods=['POST'])
def updatename(imgname):
    newname = request.form["newname"]
    if len(newname)<1:
        return "error(invalid)"
    img = models.Image.find_by_name(imgname)
    resp = img.change_name(newname)
    return "update image name from "+imgname+" to "+newname


@app.route('/showimages')
def show_images():
    images = models.Image.get_all()
    print(images)
    return render_template('images.html', images=images)


@app.route('/showimagesofuser')
@login_required
def show_images_of_user():

    images = models.Image.get_img_by_userid(current_user.id)
    print("showimagesofuser:",images)
    return render_template('images.html', images=images)


@app.route('/about')
def about():
    return render_template('about.html')

