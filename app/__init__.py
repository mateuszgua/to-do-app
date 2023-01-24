from app import views
import os
from flask import Flask
from flask_pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('mongodb://mongodb:27017/dockerapp')
db = client.tododb
userdb = client.users
