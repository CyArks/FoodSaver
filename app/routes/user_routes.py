import logging

from flask import Blueprint, jsonify, render_template, current_app, request
from flask_login import current_user, login_required

from app.Models.UserModel import User

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/', methods=['GET'])
@login_required
def view_profile():
    try:
        user_id = current_user.id  # Get the current user's ID
        print(f'User ID: {user_id}')

        user = User.query.get(user_id)  # Fetch the user's data from the database

        if user is None:
            print('User not found, returning 404')
            return jsonify({'error': 'User not found'}), 404

        print('Rendering profile template')
        return render_template('profile.html', user=user)  # Explicitly return the response
    except Exception as e:
        print(f'An exception occurred: {e}')
        return jsonify({'error': 'An internal error occurred'}), 500


@profile_blueprint.route('/api/update_profile', methods=['POST'])
@login_required
def update_profile():
    db = current_app.extensions['sqlalchemy'].db
    data = request.json
    current_user.username = data.get('username', current_user.username)
    current_user.email = data.get('email', current_user.email)
    current_user.dietary_preferences = data.get('dietary_preferences', current_user.dietary_preferences)
    current_user.notification_preferences = data.get('notification_preferences', current_user.notification_preferences)
    db.session.commit()
    logging.info({'status': 'Profile updated'}), 200
