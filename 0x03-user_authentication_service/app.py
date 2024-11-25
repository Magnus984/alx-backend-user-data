#!/usr/bin/env python3
"""Flask app
"""
from flask import Flask, jsonify, request
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
            user = auth.register_user(email, password)
            return jsonify({
                "email": f"{email}", "message": "user created" 
            })
        except ValueError:
            return jsonify({
                "message": "email already registered"
            }), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
