from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required

from app.Models.UserModel import User

profile_blueprint = Blueprint('profile', __name__)


@profile_blueprint.route('/profile', methods=['GET'])
@login_required
def view_profile():
    try:
        print('Inside view_profile function')
        user_id = current_user.id  # Get the current user's ID
        print(f'User ID: {user_id}')

        user = User.query.get(user_id)  # Fetch the user's data from the database
        print(f'User object: {user}')

        if user is None:
            print('User not found, returning 404')
            return jsonify({'error': 'User not found'}), 404

        print('Rendering profile template')
        return render_template('profile.html', user=user)  # Explicitly return the response
    except Exception as e:
        print(f'An exception occurred: {e}')
        return jsonify({'error': 'An internal error occurred'}), 500
