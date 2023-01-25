import os
from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

load_dotenv(path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", default=None)
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
