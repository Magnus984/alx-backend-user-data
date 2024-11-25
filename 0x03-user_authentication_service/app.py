#!/usr/bin/env python3
"""Flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def home() -> str:
    """GET /
    Return:
      - JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    """ POST /users
    Return:
      - JSON payload
    """
    email = request.form["email"]
    password = request.form["password"]
    if email and password:
        try:
            user = AUTH.register_user(email, password)
            return jsonify({
                "email": f"{email}", "message": "user created"
            })
        except ValueError:
            return jsonify({
                "message": "email already registered"
            }), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """POST /sessions
    """
    email = request.form["email"]
    password = request.form["password"]
    if email and password:
        if AUTH.valid_login(email, password):
            new_session = AUTH.create_session(email)
            return jsonify({
                "email": f"{email}", "message": "logged in"
            })
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
