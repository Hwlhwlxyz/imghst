'''
database
'''

import sqlite3
from flask import g

from app import app
from config import DATABASE

from . import database


class Picture:
    tablename = 'picture'
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def save(self):
        result = database.query_db('INSERT INTO picture (id, name) VALUES (?, ?)', self.id, self.name)
        return result


class User:
    tablename = 'user'

    def __init__(self,  username, password):

        self.name = username
        self.path = password


    def getAll(self):
        result = database.query_db('SELECT * FROM user')
        print(type(result))
        for value in result:
            print(value)
        return result

