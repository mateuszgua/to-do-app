from flask import Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def signup(self):

        user = {
            "_id": "",
            "name": "",
            "email": "",
            "password": ""
        }

        return jsonify(user), 200

    def __repr__(self) -> str:
        return str(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha512')

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


def check_password(password_hash, password):
    return check_password_hash(password_hash, password)
