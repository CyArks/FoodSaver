import logging
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_login import login_required, current_user
from flask import Blueprint, request, jsonify, current_app

from app.Models.UserModel import User

settings_blueprint = Blueprint('settings', __name__)


@settings_blueprint.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'message': 'New password is required'}), 400

    if user.change_password(new_password):
        # Log the successful password change
        logging.info(f'Password changed successfully for user: {current_user_id}')

        # Additional testing for invalidating JWT tokens goes here

        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        logging.error(f'Failed to change password for user: {current_user_id}')
        return jsonify({'message': 'Could not change password'}), 500


@settings_blueprint.route('/api/update_profile', methods=['POST'])
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
