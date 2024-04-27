#!/usr/bin/env python3
""" This module defines a class called User
    that inherits from Base class from SQLAlchemy
    and defines the table called users and its columns
"""
from auth import Auth
from flask import (Flask, jsonify, request, abort, redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello_world() -> str:
    """ handle the route / and return a message """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """ Register a new user """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    message = {"email": email, "message": "user created"}
    return jsonify(message)


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    """ Logs in a user and returns session ID """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    message = {"email": email, "message": "logged in"}
    response = jsonify(message)

    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    """
    Logs out a user by destroying the session_id cookie
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ This function returns the profile of the user """

    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    message = {"email": user.email}

    return jsonify(message), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    """
    POST /reset_password
    """
    try:
        email = request.form['email']
    except KeyError:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    message = {"email": email, "reset_token": reset_token}

    return jsonify(message), 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """ This function updates the password of a user
    """
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
    except KeyError:
        abort(400)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    message = {"email": email, "message": "Password updated"}
    return jsonify(message), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
