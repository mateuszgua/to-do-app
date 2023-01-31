import os
from flask import Flask
from flask_pymongo import MongoClient
from flask_session import Session

from app.config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

user = Config.USER
password = Config.PASSWORD
password = Config.MONGODB_URI

client = MongoClient(f"mongodb+srv://{user}:{password}@cluster0.e4jzd92.mongodb.net/?retryWrites=true&w=majority", connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db = client.tododb
collection_user = db.users
collection_task = db.tasks

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from app import views