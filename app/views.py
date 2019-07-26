from flask import render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from app import app

from . import models


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

@app.route('/')
@app.route('/index')
def index():
    user = {'name': 'user1'}  # fake user
    return render_template("index.html",
                           user=user)


@app.route('/u')
def user():
     # fake user
    user = models.User('user1', 'ps1')
    print(user.getAll())
    return user.getAll()[0]


@app.route('/upload', methods=['POST', 'GET'])
def upload():

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')

