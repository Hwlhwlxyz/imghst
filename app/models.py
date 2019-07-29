'''
database
'''

import sqlite3
from flask import g, config
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import render_template, request

from app import app
from config import DATABASE

from . import database

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class Image:
    tablename = 'image'
    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(Image.tablename))
        return result


    @staticmethod
    def save(requestfiles):
        print(requestfiles, requestfiles.filename)
        filename = requestfiles.filename
        result = database.query_db('INSERT INTO {} VALUES (?)'.format(Image.tablename), [filename])
        print(result)
        filename = photos.save(requestfiles)
        return filename

    @staticmethod
    def find_by_name(name):
        result = database.query_db('SELECT * FROM {} WHERE name=?'.format(Image.tablename), [name], one=True)
        imageResult = Image(result['name'])
        return imageResult

    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(Image.tablename))
        return result

    def get_img(self):
        img = None
        path = app.config['UPLOADED_PHOTOS_DEST']+'/' + self.name
        with open(path, 'rb') as f:
            img = f.read()
        return img

class User:
    tablename = 'user'

    def __init__(self, username, password):
        self.name = username
        self.path = password



    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(User.tablename))
        return result

