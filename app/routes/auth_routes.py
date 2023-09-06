from flask_jwt_extended import create_access_token
from flask_login import login_required, logout_user, current_user
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

            return jsonify({'msg': 'Login successful'}), 200

        return jsonify({'error': 'Invalid username or password'}), 401

    # Handle GET request
    if request.method == 'GET':
        return render_template('login.html')


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@main.route('/register', methods=['GET', 'POST'])
def register():
    db = current_app.extensions['sqlalchemy'].db
    if request.method == 'POST':
        data = request.form
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        logging.info({"msg": "User registered successfully"})
        return render_template('dashboard.html', username=username), 200

    return render_template('register.html')