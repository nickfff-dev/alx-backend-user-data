#!/usr/bin/env python3
"""Session authentication module."""
from flask import request, jsonify, abort
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'])
def login():
    """Login route."""
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email == '' or email is None:
        return jsonify({"error": "email missing"}), 400
    if not password or password == '' or password is None:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    session_name = os.getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)
    return response


@app_views.route('/auth_session/logout', methods=['DELETE'])
def logout():
    """Logout route."""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
