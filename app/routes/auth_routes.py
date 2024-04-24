import logging

from flask_jwt_extended import create_access_token
from flask_login import login_required, logout_user
from flask import Blueprint, jsonify, make_response, render_template, current_app, request, redirect, url_for
from app.Models.UserModel import User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    db = current_app.extensions['sqlalchemy'].db
    print(f"SQLAlchemy db instance: {db}")

    if request.method == 'POST':
        # Handle login
        username = request.form['username']
        password = request.form['password']

        # Fetch user from database
        user = User.query.filter_by(username=username).first()

        # Validate user
        if user and user.check_password(password):
            access_token = create_access_token(identity=username)

            # Create response object
            resp = make_response(render_template('dashboard.html'))

            # Set cookie with the access_token
            resp.set_cookie('access_token', access_token)

            return redirect(url_for('profile.view_profile'))

        # ToDo: Use Java script to handle this error
        return jsonify({'error': 'Invalid username or password'}), 401

    # Handle GET request
    if request.method == 'GET':
        return render_template('login.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    db = current_app.extensions['sqlalchemy'].db

    if request.method == 'POST':
        data = request.form
        email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)

        if User.email_already_exists(email):
            # ToDo: Trigger javascript code to display that the email is already in use
            return jsonify({'error': 'Email already in use!'}), 000  # ToDo: update return code

        if not User.username_is_unique(username):
            # ToDo: Trigger javascript code to display that the username is already in use
            return jsonify({'error': 'Username already in use!'}), 000  # ToDo: update return code

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        logging.info({"msg": "User registered successfully"})
        return render_template('dashboard.html', username=username), 200

    return render_template('register.html')
