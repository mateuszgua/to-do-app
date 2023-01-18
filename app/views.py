from flask import jsonify, request, render_template, redirect, url_for
from bson.objectid import ObjectId
import socket
from flask_pymongo import MongoClient

from app import app
from app import db

@app.route("/")
def index():
    hostname = socket.gethostname()
    return jsonify(message="Welcome to Tasks app! I am running inside {} pod!".format(hostname))

@app.route("/tasks")
def get_all_tasks():
    _tasks = db.tododb.find()
    tasks = [task for task in _tasks]

    return render_template('index.html', tasks=tasks)

@app.route("/add", methods=["POST"])
def create_task():
    task_doc = {
        'name': request.form["name"],
        'description': request.form["description"],
        'start_date': request.form["start_date"],
        'end_date': request.form["end_date"],
        'status': request.form["status"],
        'priority': request.form["priority"],
    }
    db.tododb.insert_one(task_doc)
    return redirect(url_for('get_all_tasks'))

@app.route("/task/<id>", methods=["PUT"])
def update_task(id):
    data = request.get_json(force=True)["task"]
    response = db.task.update_one({"_id": ObjectId(id)}, {"$set":{"task":data}})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No task found!"
    return jsonify(message=message)

@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    response = db.task.delete_one({"_id":ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No task found!"
    return jsonify(message=message)

@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    db.task.remove()
    return jsonify(message="All Tasks deleted!")


