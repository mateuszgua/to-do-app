import os
from flask import Flask
from flask_pymongo import MongoClient
from app import models

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'
client = MongoClient('mongodb://mongodb:27017/dockerapp')
db = client.tododb
userdb = client.users

from app import views