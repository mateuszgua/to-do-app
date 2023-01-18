from flask import jsonify, request, render_template, redirect, url_for
from bson.objectid import ObjectId
import socket
from flask_pymongo import MongoClient

from app import app
from app import db


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/panel")
def panel():
    _tasks = db.tododb.find()
    tasks = [task for task in _tasks]

    return render_template('panel.html', tasks=tasks)


@app.route("/add", methods=["POST"])
def create_task():
    task_doc = {
        'id': ObjectId(),
        'name': request.form["name"],
        'description': request.form["description"],
        'start_date': request.form["start_date"],
        'end_date': request.form["end_date"],
        'status': request.form["status"],
        'priority': request.form["priority"],
    }
    db.tododb.insert_one(task_doc)
    return redirect(url_for('panel'))


@app.route("/task/<id>", methods=["PUT"])
def update_task(id):
    task_doc = {
        'name': request.form["name"],
        'description': request.form["description"],
        'start_date': request.form["start_date"],
        'end_date': request.form["end_date"],
        'status': request.form["status"],
        'priority': request.form["priority"],
    }
    response = db.tododb.update_one({"id": ObjectId(id)},
                                    {"$set": task_doc})
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No task found!"
    return render_template('panel.html', message=message)


@app.route("/task/<id>", methods=["DELETE"])
def delete_task(id):
    response = db.tododb.delete_one({"id": ObjectId(id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No task found!"
    return render_template('panel.html', message=message)


@app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    response = db.tododb.remove()
