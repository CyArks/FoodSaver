from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User  # Assuming you have a User model
import logging

# Create Blueprint
main = Blueprint('main', __name__)

# Logger setup
logger = logging.getLogger(__name__)

@main.route('/')
def home():
    return jsonify({'message': 'Welcome to the Home Page'})

@main.route('/secure', methods=['GET'])
@jwt_required()
def secure_route():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    
    if not user:
        logger.warning(f'User not found: {current_user_id}')
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({'message': 'This is a secure route'})

@main.route('/admin', methods=['GET'])
@jwt_required()
def admin_route():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)

    if not user.has_role('admin'):
        logger.warning(f'Unauthorized access attempt by: {current_user_id}')
        return jsonify({'message': 'You do not have permission to access this route'}), 403

    return jsonify({'message': 'This is an admin route'})

@main.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    
    data = request.get_json()
    new_password = data['new_password']
    
    if not user.change_password(new_password):
        logger.error(f'Failed to change password for user: {current_user_id}')
        return jsonify({'message': 'Could not change password'}), 500
    
    # Additional code for invalidating JWT tokens goes here
    
    return jsonify({'message': 'Password changed successfully'})

@main.errorhandler(404)
def handle_404(error):
    logger.warning('404 error occurred')
    return jsonify({'error': 'Resource not found'}), 404

@main.errorhandler(500)
def handle_500(error):
    logger.critical('500 error occurred', exc_info=True)
    return jsonify({'error': 'An internal error occurred'}), 500
