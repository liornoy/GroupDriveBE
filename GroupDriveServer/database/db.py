from flask_mongoengine import MongoEngine
from mongoengine import connect

def initialize_db(app):
    connect('groupdrive', host='127.0.0.1', port=27017)