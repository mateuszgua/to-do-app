import os
from flask import Flask
from flask_pymongo import MongoClient
from flask_session import Session

from app.config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

client = MongoClient('mongodb://mongodb:27017/dockerapp')
db = client.tododb
collection_user = db.users
collection_task = db.tasks

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from app import views