#!/usr/bin/env python3
""" User authentication service"""
from flask import Flask, jsonify, request, Response, abort, redirect
from auth import Auth
from user import User


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    Defines the root route of the Flask application.

    Returns:
        str: A JSON response with a welcome message.
    """

    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """
    Registers a new user with the provided email and password.

    Retrieves the email and password from the request form data, attempts to
    register the user,
    and returns a JSON response with the newly created user's email and a
    success message.
    If the email is already registered, returns a JSON error response with a
    400 status code.

    Returns:
        tuple[Response, int]: A JSON response with the user's email and a
        success message, or a JSON error response with a 400 status code.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": user.email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Handles the POST request to the '/sessions' route for user login.

    Retrieves the email and password from the request form data.
    Prints the email and password for debugging purposes.
    Validates the login credentials using the AUTH object.
    If the login is valid, creates a session ID, sets a cookie with the
    session ID,
    and returns a JSON response with the user's email and a success message.
    If the login is invalid, prints an error message and aborts with a 401
    status code.

    Parameters:
        None

    Returns:
        A Flask response object with a JSON payload containing the user's
        email and a success message,
        or a Flask abort object with a 401 status code.

    Raises:
        None
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        if not AUTH.valid_login(email, password):
            abort(401)
        session_id = AUTH.create_session(email)
        # session_id_str = str(session_id)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response

    except ValueError:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Handles the DELETE request to the '/sessions' route for user logout.

    Retrieves the session ID from the request cookies.
    Validates the session ID and retrieves the associated user.
    Destroys the user session using the AUTH object.
    Redirects the user to the root URL and clears the session ID cookie.

    Parameters:
        None

    Returns:
        A Flask response object with a redirect to the root URL,
        or a Flask abort object with a 403 status code.

    Raises:
        None
    """
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    response = redirect('/')
    response.set_cookie('session_id', '', expires=0)
    return response


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Retrieves the user's email from the session ID stored in a cookie.

    This function is a route handler for the '/profile' endpoint. It accepts
    GET requests and does not require any parameters.

    Returns:
        A JSON response containing the user's email.

    Raises:
        403: If the session ID is not found in the cookie or if the user is
        not found in the database.

    Raises:
        Exception: If an error occurs during the execution of the function.
    """
    try:
        session_id = request.cookies.get('session_id')
        if session_id is None:
            abort(403)

        user = AUTH.get_user_from_session_id(session_id)
        if user is None:
            abort(403)

        return jsonify({"email": user.email}), 200

    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password_token() -> str:
    """
    Handles the POST request to the '/reset_password' route for generating a
    reset password token.

    Retrieves the email from the request form data, attempts to generate a
    reset password token,
    and returns a JSON response with the email and the generated reset token.

    Parameters:
        None

    Returns:
        A JSON response containing the email and the generated reset token.

    Raises:
        403: If an error occurs during the execution of the function.
    """
    try:
        email = request.form.get('email')
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Handles the PUT request to the '/reset_password' route for updating a
    user's password.

    Retrieves the email, reset token, and new password from the request form
    data.
    Attempts to update the user's password using the provided reset token and
    new password.
    Returns a JSON response with the user's email and a success message if the
    update is successful.
    Raises a 403 error if an exception occurs during the execution of the
    function.

    Parameters:
        email (str): The email of the user to update the password for.
        reset_token (str): The reset token used to identify the user.
        new_password (str): The new password to be updated.

    Returns:
        A JSON response containing the user's email and a success message.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
