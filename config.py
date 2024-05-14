import os

class Config(object):
    # ...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cannot-be-guess'
    
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:12345@localhost:5432/manage"
    SQLALCHEMY_TRACK_MODIFICATIONS = False