from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.cache_manager import get_offer, invalidate_offer_cache
from .permissions import admin_permission
from .permissions import require_admin
from .rate_limiter import limiter
from your_app.models import Recipe, db
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

@app.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return 'Admin page'

@app.route('/some_path')
@limiter.limit("5 per minute")  # Override the default rate limit for this route
def some_route():
    return 'This is some route.'

@app.route('/offer/<int:offer_id>')
def show_offer(offer_id):
    offer = get_offer(offer_id)
    return jsonify(offer)

@app.route('/api/search_recipes', methods=['GET'])
def search_recipes():
    query = db.session.query(Recipe)

    # Filtering by ingredients
    ingredients = request.args.get('ingredients')
    if ingredients:
        query = query.filter(Recipe.ingredients.ilike(f"%{ingredients}%"))

    # Filtering by time
    max_time = request.args.get('max_time')
    if max_time:
        query = query.filter(Recipe.total_time <= max_time)

    # Sorting by rating
    sort_by_rating = request.args.get('sort_by_rating')
    if sort_by_rating:
        query = query.order_by(Recipe.rating.desc())
        
    # Add more filters as needed
    
    recipes = query.all()
    return jsonify([recipe.serialize() for recipe in recipes])  # Assuming you have a serialize method in your Recipe model

@app.route('/offer/<int:offer_id>')
def show_offer(offer_id):
    offer = get_offer(offer_id)
    return jsonify(offer)

@app.route('/offer/update/<int:offer_id>', methods=['POST'])
def update_offer(offer_id):
    # ... update offer logic ...
    invalidate_offer_cache(offer_id)
    return jsonify({"status": "Offer updated and cache invalidated."})

@main.errorhandler(404)
def handle_404(error):
    logger.warning('404 error occurred')
    return jsonify({'error': 'Resource not found'}), 404

@main.errorhandler(500)
def handle_500(error):
    logger.critical('500 error occurred', exc_info=True)
    return jsonify({'error': 'An internal error occurred'}), 500
