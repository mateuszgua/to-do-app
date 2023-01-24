from flask import jsonify, request, render_template, redirect, url_for, session, flash
from bson.objectid import ObjectId
import socket
from flask_pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import bcrypt
import uuid

from app import app
from app import db, userdb
from app.models import check_password


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/panel")
def panel():
    _tasks = db.tododb.find()
    tasks = [task for task in _tasks]

    return render_template('panel.html', tasks=tasks)


def start_session(user):
    del user["password"]
    session["logged_in"] = True
    session["user"] = user
    return jsonify(user), 200


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        users = userdb.users
        login_user = users.find_one({"name": request.form["name"]})

        if login_user:
            if pbkdf2_sha256.verify(request.form["password"], login_user["password"]):
                start_session(login_user)
                return redirect(url_for("panel"))

            flash("Invalid username or password!")
            return render_template("login.html")

        flash("Invalid username")
        return redirect(url_for("login"))

    return render_template("login.html")


@ app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form["name"],
            "email": request.form["email"],
            "password": request.form["password"]
        }

        users = userdb.users
        user["password"] = pbkdf2_sha256.encrypt(user["password"])
        existing_user = users.find_one({"name": user["name"]})

        if existing_user is None:
            users.insert_one(user)
            start_session(user)
            return redirect(url_for("panel"))

        flash("That username: " + user["name"] + " already exist!")
        return redirect(url_for('register'))

    return render_template("register.html")


@ app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
        flash("Task updated successfully!")
    else:
        flash("No task found!")
    return redirect(url_for('panel'))


@ app.route("/task/<task_id>", methods=["POST"])
def delete_task(task_id):
    response = db.tododb.delete_one({"id": ObjectId(task_id)})
    if response.deleted_count:
        flash("Task deleted successfully!")
    else:
        flash("No task found!")
    return redirect(url_for('panel'))


@ app.route("/tasks/delete", methods=["POST"])
def delete_all_tasks():
    response = db.tododb.remove()
