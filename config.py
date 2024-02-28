import os
from sqlalchemy import create_engine
import urllib

class Config(object):
    SECRET_KEY='Clave_Nueva'
    SESSION_COOKIE_SECURE=False


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://yaz:12345678@127.0.0.1/pruba'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
#crear nuevo usuario en mysql