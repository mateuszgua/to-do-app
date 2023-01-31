from flask import jsonify, request, render_template, redirect, url_for, session, flash, abort
from bson.objectid import ObjectId
from passlib.hash import pbkdf2_sha256
import uuid

from app import app
from app import collection_task, collection_user
from app.my_error import LoadTasksProblem, LoadUserProblem
from app.my_error import DatabaseWriteUserError, DatabaseWriteTaskError, DatabaseEditTaskError, DatabaseDeleteTaskError


@app.route("/")
def index():
    is_user_login = None
    return render_template("index.html", is_user_login=is_user_login)


@app.route("/panel")
def panel():
    try:
        if "user" not in session:
            is_user_login = None
            # return redirect(url_for("login"))
            flash("Problem with get user from session!")
            return render_template("login.html")
        is_user_login = session["user"]
        user_name = session["user"]["name"]
        tasks = [task for task in collection_task.find({"user": user_name})]
    except LoadTasksProblem:
        error_description = LoadTasksProblem()
        internal_server_error(error_description)
        abort(500, error_description)
    else:
        return render_template("panel.html", tasks=tasks, user_name=user_name, is_user_login=is_user_login)


def start_session(user):
    del user["password"]
    session["logged_in"] = True
    session["user"] = user
    return jsonify(user), 200


@ app.route("/login", methods=["POST", "GET"])
def login():
    is_user_login = None
    if request.method == "POST":
        try:
            user = collection_user.find_one({"name": request.form["name"]})

            if user:
                if pbkdf2_sha256.verify(request.form["password"], user["password"]):
                    start_session(user)
                    return redirect(url_for("panel"))

                flash("Invalid username or password!")
                return render_template("login.html")

            flash("Invalid username")
            return render_template("login.html")
        except LoadUserProblem:
            error_description = LoadUserProblem()
            internal_server_error(error_description)
            abort(500, error_description)
    return render_template("login.html", is_user_login=is_user_login)


@ app.route("/register", methods=["POST", "GET"])
def register():
    is_user_login = None
    if request.method == "POST":
        try:
            user = {
                "_id": uuid.uuid4().hex,
                "name": request.form["name"],
                "email": request.form["email"],
                "password": request.form["password"]
            }

            user["password"] = pbkdf2_sha256.encrypt(user["password"])
            existing_user = collection_user.find_one({"name": user["name"]})

            if existing_user is None:
                collection_user.insert_one(user)
                start_session(user)
                return redirect(url_for("panel"))

            flash("That username: " + user["name"] + " already exist!")
            return redirect(url_for('register'))
        except DatabaseWriteUserError:
            error_description = DatabaseWriteUserError()
            page_not_found(error_description)
            abort(404, error_description)
    return render_template("register.html", is_user_login=is_user_login)


@ app.route("/logout")
def logout():
    session["logged_in"] = False
    session.pop("user", None)
    return redirect("/")


@ app.route("/add", methods=["POST"])
def create_task():
    try:
        task_doc = {
            'id': ObjectId(),
            'user': session["user"]["name"],
            'name': request.form["name"],
            'description': request.form["description"],
            'start_date': request.form["start_date"],
            'end_date': request.form["end_date"],
            'status': request.form["status"],
            'priority': request.form["priority"],
        }
        collection_task.insert_one(task_doc)
    except DatabaseWriteTaskError:
        error_description = DatabaseWriteTaskError()
        page_not_found(error_description)
        abort(404, error_description)
    else:
        return redirect(url_for('panel'))


@ app.route("/task/edit/<task_id>", methods=["POST"])
def update_task(task_id):
    try:
        edit_name = request.form["name"]
        edit_description = request.form["description"]
        edit_start_date = request.form["start_date"]
        edit_end_date = request.form["end_date"]
        edit_status = request.form["status"]
        edit_priority = request.form["priority"]
        response = collection_task.update_many({"id": ObjectId(task_id)},
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
    except DatabaseEditTaskError:
        error_description = DatabaseEditTaskError()
        page_not_found(error_description)
        abort(404, error_description)
    else:
        return redirect(url_for('panel'))


@ app.route("/task/<task_id>", methods=["POST"])
def delete_task(task_id):
    try:
        response = collection_task.delete_one({"id": ObjectId(task_id)})
        if response.deleted_count:
            flash("Task deleted successfully!")
        else:
            flash("No task found!")
    except DatabaseDeleteTaskError:
        error_description = DatabaseDeleteTaskError()
        page_not_found(error_description)
        abort(404, error_description)
    else:
        return redirect(url_for('panel'))


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e)


@ app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', e=e)
