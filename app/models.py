'''
database
'''
import hmac
import sqlite3
from flask import g, config
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import render_template, request
from flask_login import UserMixin, LoginManager, login_manager

import hashlib

from app import app


from . import database

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


class Image:
    tablename = 'image'
    def __init__(self, name):
        self.name = name
        self.userid = None

    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(Image.tablename))
        return result

    @staticmethod
    def get_img_by_userid(userid):
        result = database.query_db('SELECT * FROM {} WHERE userid=?'.format(Image.tablename), [userid])
        return result

    @staticmethod
    def save(requestfiles, userid):
        currentuser = User.get_user(userid)
        if currentuser:
            print(requestfiles, requestfiles.filename)
            #filename = requestfiles.filename
            filename = photos.save(requestfiles)
            #photos.save(requestfiles,folder='',name=None)
            database.query_db('INSERT INTO {}(name, userid) VALUES (?,?)'.format(Image.tablename), (filename, userid))
            return filename
        else:
            print('user not exist')

        return None

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
        print(self.name)
        path = app.config['UPLOADED_PHOTOS_DEST']+'/' + self.name
        with open(path, 'rb') as f:
            img = f.read()
        return img




class User(UserMixin):
    tablename = 'user'

    def __init__(self, username, password, email, id=-1):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    @staticmethod
    def hash_password(password):
        myhmac = hmac.new(app.secret_key.encode(), password.encode(), digestmod='MD5')
        return myhmac.hexdigest()

    def get_id(self):
        result = database.query_db('SELECT rowid, * FROM {} WHERE username=?'.format(User.tablename), [self.username])
        if result:
            result = result[0]
        if len(result) > 0:
            self.id = result['rowid']
            return self.id
        else:
            return None

    def verify_password(self, password):
        if self.password is None:
            return False
        #return check_password_hash(self.password_hash, password)
        #self.password has been hashed
        return self.password == self.hash_password(password)

    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(User.tablename))
        return result

    @staticmethod
    def get_user(user_id):
        print("user_id",user_id)
        result = database.query_db('SELECT rowid, * FROM {} WHERE rowid=?'.format(User.tablename), [user_id])
        if result:
            result = result[0]
        if len(result) > 0:
            result_user = User(result['username'], result['password'], result['email'], user_id)
            return result_user
        else:
            return None

    @staticmethod
    def get_user_by_email(email):
        result = database.query_db('SELECT rowid, * FROM {} WHERE email=?'.format(User.tablename), [email])
        print(result, email)
        if result:
            result = result[0]
        if len(result) > 0:
            result_user = User(result['username'], result['password'], result['email'], result['rowid'])
            return result_user
        else:
            return None




    def save(self):
        hash_password = self.hash_password(self.password)
        result = database.query_db('INSERT INTO {}(username, password, email) VALUES (?,?,?)'.format(User.tablename), (self.username, hash_password, self.email))
        if result:
            result = result[0]
        if len(result) > 0:

            result_user = User(result['username'], result['password'], result['email'])
            return result_user
        else:
            return None

