from app import app
from flask import jsonify
import socket

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(message="Welcome to Tasks app! I am running inside {} pod!".format(hostname))