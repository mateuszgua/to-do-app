from flask import jsonify, request, render_template, redirect, url_for, session
from bson.objectid import ObjectId
import socket
from flask_pymongo import MongoClient
import bcrypt

from app import app
from app import db, userdb


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/panel")
def panel():
    _tasks = db.tododb.find()
    tasks = [task for task in _tasks]

    return render_template('panel.html', tasks=tasks)


@app.route("/login", methods=["POST"])
def login():
    users = userdb.users
    login_user = users.find_one({"name": request.form["name"]})

    if login_user:
        if bcrypt.hashpw(request.form["password"].encode("utf-8"), login_user["password"].encode("utf-8")) == login_user["password"].encode("utf-8"):
            session["name"] = request.form["name"]
            return redirect(url_for("panel"))
    else:
        return "Invalid username or password"
    
    return render_template("login.html")

@ app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # TODO dodać bazę user
        users = userdb.users
        existing_user = users.find_one({"name": request.form["name"]})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form["password"].encode("utf-8"), bcrypt.gensalt())
            users.insert_one({"name": request.form["name"], "password": hashpass})
            # session["name"] = request.form["name"]
            return redirect(url_for("panel"))

        return "That username already exist!"

    return render_template("register.html")


@ app.route("/add", methods=["POST"])
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


@ app.route("/task/edit/<task_id>", methods=["POST"])
def update_task(task_id):
    edit_name = request.form["name"]
    edit_description = request.form["description"]
    edit_start_date = request.form["start_date"]
    edit_end_date = request.form["end_date"]
    edit_status = request.form["status"]
    edit_priority = request.form["priority"]
    response = db.tododb.update_many({"id": ObjectId(task_id)},
                                     {"$set": {'name': edit_name,
                                               'description': edit_description,
                                               'start_date': edit_start_date,
                                               'end_date': edit_end_date,
                                               'status': edit_status,
                                               'priority': edit_priority}},)
    if response.matched_count:
        message = "Task updated successfully!"
    else:
        message = "No task found!"
    return redirect(url_for('panel', message=message))


@ app.route("/task/<task_id>", methods=["POST"])
def delete_task(task_id):
    response = db.tododb.delete_one({"id": ObjectId(task_id)})
    if response.deleted_count:
        message = "Task deleted successfully!"
    else:
        message = "No task found!"
    return redirect(url_for('panel', message=message))


@ app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    response = db.tododb.remove()
