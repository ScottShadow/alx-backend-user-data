#!/usr/bin/env python3
"""
Session_auth View Module
"""
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ POST /api/v1/auth_session/login
    Return:
      - 200
      - 400
    """
    # from api.v1.views import index
    from models.user import User
    from flask import request, jsonify
    from flask_babel import _
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or len(email) == 0:
        return jsonify({'error': 'email missing'}), 400
    if password is None or len(password) == 0:
        return jsonify({'error': 'password missing'}), 400

    user = User.search({'email': email})
    if user is None or len(user) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    if not user[0].is_valid_password(password):
        return jsonify({'error': 'wrong password'}), 401

    try:
        from api.v1.app import auth
        from models.base import Base
        import os
        for u in user:
            session_id = auth.create_session(u.id)
            session_name = os.environ.get("SESSION_NAME")
            response = jsonify(u.to_json())
            response.set_cookie(session_name, session_id)
            return response
    except Exception as e:
        return jsonify({'error': 'Forbidden'}), 403

    return jsonify({})


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ DELETE /api/v1/auth_session/logout
    Return:
      - 200
      - 403
    """
    # from api.v1.views import index
    from api.v1.app import auth
    from flask import request, jsonify

    if request:
        auth.destroy_session(request)
    return jsonify({})
