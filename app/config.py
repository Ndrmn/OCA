import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CSRF_ENABLED = True
    SECRET_KEY = '0987654321'
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.bd"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
