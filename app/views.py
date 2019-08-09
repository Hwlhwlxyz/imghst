from flask import render_template, request, jsonify, Response

from app import app, database

from . import models


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/u')
def user():
    # fake user
    user = models.User('user1', 'ps1')
    print(user.get_all())
    data = user.get_all()
    return jsonify(data)





@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = models.Image.save(request.files['photo'])
        print(filename)
    return render_template('upload.html')


@app.route('/uploadbydropzone', methods=['POST', 'GET'])
def dropzoneupload():
    print(request.files)
    if request.method == 'POST':
        for f in request.files.getlist('file'):
            print(f.filename)
    return render_template('dropzone.html')


@app.route('/image/<imgname>')
def return_img_stream(imgname):
    resp = Response(models.Image(models.Image.find_by_name(imgname).name).get_img(), mimetype="image/jpeg")
    return resp

@app.route('/image')
def get_images():
    data = models.Image.get_all()
    return jsonify(data)

@app.route('/showimages')
def show_images():
    images = models.Image.get_all()
    return render_template('images.html', images=images)
