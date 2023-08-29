from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.cache_manager import get_offer, invalidate_offer_cache
from .permissions import admin_permission
from flask_login import login_required, current_user
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

@app.route('/api/track_waste', methods=['POST'])
@login_required
def track_waste():
    data = request.json
    waste_action = WasteTracking(
        food_item_id=data['food_item_id'],
        action=data['action'],
        user_id=current_user.id
    )
    db.session.add(waste_action)
    
    def calculate_sustainability_score(user_id):
    waste_actions = WasteTracking.query.filter_by(user_id=user_id).all()
    score = 0
    for action in waste_actions:
        if action.action == "Used":
            score += 10
        elif action.action == "Thrown":
            score -= 5
    return score

# Update the sustainability score here based on the action
new_score = calculate_sustainability_score(current_user.id)
current_user.sustainability_score = new_score
    
    db.session.commit()
    return jsonify({'status': 'Waste tracked', 'new_score': new_score}), 201

@app.route('/api/recipes', methods=['POST'])
@login_required
def create_recipe():
    data = request.json
    new_recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        steps=data['steps'],
        user_id=current_user.id
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'status': 'Recipe created'}), 201

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.serialize() for recipe in recipes]), 200

@app.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_single_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify(recipe.serialize()), 200

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

@app.route('/api/meal_plan', methods=['POST'])
@login_required
def create_meal_plan():
    recipe_ids = request.json['recipe_ids']
    new_plan = MealPlan(user_id=current_user.id, recipe_ids=recipe_ids)
    db.session.add(new_plan)
    db.session.commit()
    return jsonify({'status': 'Meal plan created'}), 201

@app.route('/api/meal_plan', methods=['GET'])
@login_required
def get_meal_plans():
    plans = MealPlan.query.filter_by(user_id=current_user.id).all()
    return jsonify([plan.serialize() for plan in plans]), 200

@app.route('/api/grocery_list', methods=['POST'])
@login_required
def create_grocery_list():
    items = request.json['items']
    new_list = GroceryList(user_id=current_user.id, items=items)
    db.session.add(new_list)
    db.session.commit()
    return jsonify({'status': 'Grocery list created'}), 201

@app.route('/api/grocery_list', methods=['GET'])
@login_required
def get_grocery_lists():
    lists = GroceryList.query.filter_by(user_id=current_user.id).all()
    return jsonify([list.serialize() for list in lists]), 200

@main.errorhandler(404)
def handle_404(error):
    logger.warning('404 error occurred')
    return jsonify({'error': 'Resource not found'}), 404

@main.errorhandler(500)
def handle_500(error):
    logger.critical('500 error occurred', exc_info=True)
    return jsonify({'error': 'An internal error occurred'}), 500
