'''
database
'''
import hmac

from flask_uploads import UploadSet, configure_uploads, IMAGES

from flask_login import UserMixin, LoginManager, login_manager

import os

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
    def get_request_file_size(request_file_object):
        try:
            pos = request_file_object.tell()
            request_file_object.seek(0, 2)  # seek to end
            size = request_file_object.tell()
            request_file_object.seek(pos)  # back to original position
            return size
        except (AttributeError, IOError):
            pass
            # in-memory file object that doesn't support seeking or tell
        return 0  # assume small enough

    @staticmethod
    def check_file_limitation(request_file_object):
        size = Image.get_request_file_size(request_file_object)
        print("SIZE:", size)
        result = database.query_db('SELECT SUM(size) FROM {}'.format(Image.tablename))
        print(result)
        size_of_exist_files = result[0]['SUM(size)']
        print("*" * 10)
        print(result, app.config['USAGE_OF_FLASK'], size_of_exist_files)
        print("*" * 10)
        if size_of_exist_files:
            if size > app.config['USAGE_OF_FLASK'] - size_of_exist_files:
                # TODO response
                print("no space")
                return False
        return True

    @staticmethod
    def save(requestfile, userid):
        currentuser = User.get_user(userid)
        size = Image.get_request_file_size(requestfile)
        if Image.check_file_limitation(requestfile):
            if currentuser:
                print(requestfile, requestfile.filename)
                # filename = requestfiles.filename
                filename = photos.save(requestfile)
                # photos.save(requestfiles,folder='',name=None)
                database.query_db('INSERT INTO {}(name, userid, size) VALUES (?,?,?)'.format(Image.tablename),
                                  (filename, userid, size))
                return filename
            else:
                print('user not exist')

        return None

    @staticmethod
    def find_by_name(name):
        result = database.query_db('SELECT * FROM {} WHERE name=?'.format(Image.tablename), [name], one=True)
        if result:
            imageResult = Image(result['name'])
            return imageResult
        else:
            return None

    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(Image.tablename))
        return result

    def get_img(self):
        img = None
        print(self.name)
        path = app.config['UPLOADED_PHOTOS_DEST'] + '/' + self.name
        with open(path, 'rb') as f:
            img = f.read()
        return img

    def checkfilename(self, full_newname):
        existfile = Image.find_by_name(full_newname)
        print('existfile:', existfile)
        if existfile:
            print('the file is exist')
            return False
        return True

    # TODO handle error
    # newname without ext
    def change_name(self, newname):
        file_name, file_extension = os.path.splitext(self.name)
        full_newname = newname + file_extension
        if self.checkfilename(full_newname):
            result = database.query_db('UPDATE {} set name=? WHERE name=?'.format(Image.tablename),
                                       (full_newname, self.name))
            file_name, file_extension = os.path.splitext(self.name)
            # change file name
            print(newname + file_extension)
            os.rename(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], self.name),
                      os.path.join(app.config['UPLOADED_PHOTOS_DEST'], full_newname))
        else:
            return "upload failed"
        return result

    # TODO handle error
    def delete(self):
        print(self.name, "delete~")

        result = database.query_db('DELETE FROM {} WHERE name=?'.format(Image.tablename), [self.name])

        os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], self.name))
        return result


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
        # return check_password_hash(self.password_hash, password)
        # self.password has been hashed
        return self.password == self.hash_password(password)

    @staticmethod
    def get_all():
        result = database.query_db('SELECT * FROM {}'.format(User.tablename))
        return result

    @staticmethod
    def get_user(user_id):
        print("user_id", user_id)
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
        result = database.query_db('INSERT INTO {}(username, password, email) VALUES (?,?,?)'.format(User.tablename),
                                   (self.username, hash_password, self.email))
        if result:
            result = result[0]
        if len(result) > 0:

            result_user = User(result['username'], result['password'], result['email'])
            return result_user
        else:
            return None
