import os

current_path = os.path.dirname(os.path.realpath(__file__))
db_path = 'sqlite:///' + current_path + '//project.db'


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
    JWT_SECRET_KEY = 'test'
