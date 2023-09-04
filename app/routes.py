import os
import logging
import requests
from functools import wraps
from marshmallow import validate
from app.models import Recipe, db
from app.rate_limiter import limiter
from app.permissions import admin_permission
from jsonschema import validate, ValidationError
from flask_login import login_required, current_user
from app.cache_manager import get_offer, invalidate_offer_cache
from app.models import User, Product, GroceryList, MealPlan, WasteTracking
from flask import Blueprint, jsonify, request, render_template, make_response, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, decode_token

# Create Blueprint
main = Blueprint('main', __name__)
auth_blueprint = Blueprint('auth', __name__)

# Logger setup
logger = logging.getLogger(__name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = decode_token(token)
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator


@main.route('/')
def home():
    resp = make_response(render_template('layout.html'))
    # Modify resp here if needed, e.g., set a cookie
    return resp, 200


@main.route('/debug')
def debug_route():
    template_folder_path = os.path.join(os.getcwd(), 'templates')
    return f"Template folder path: {template_folder_path}"


@main.route('/login', methods=['GET', 'POST'])
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


@main.route('/api/fetch_deals', methods=['GET'])
def fetch_deals():
    # For demonstration purposes, we'll assume "Too Good To Go" has an endpoint like this:
    too_good_to_go_data = requests.get("https://api.toogoodtogo.com/deals").json()

    # Similarly, for local stores, you could add more API calls
    # local_store_data = requests.get("https://api.localstore.com/deals").json()

    # You might want to process the data before sending it to the frontend
    processed_data = {
        "too_good_to_go": too_good_to_go_data,
        # "local_store": local_store_data
    }

    logging.info(processed_data), 200


waste_schema = {
    "type": "object",
    "properties": {
        "food_item_id": {"type": "string"},
        "action": {"type": "string", "enum": ["Used", "Thrown"]},
    },
    "required": ["food_item_id", "action"]
}


@main.route('/api/track_waste', methods=['POST'])
@login_required
def track_waste():
    db = current_app.extensions['sqlalchemy'].db
    data = request.json
    logging.info(f"Received waste tracking data: {data}")

    try:
        validate(instance=data, schema=waste_schema)
    except ValidationError as e:
        logging.info({"error": str(e)}), 400

    waste_action = WasteTracking(
        food_item_id=data['food_item_id'],
        action=data['action'],
        user_id=current_user.id
    )
    db.session.add(waste_action)
    logging.info(f"Waste tracking for user {current_user.id} successful.")

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
    logging.info({'status': 'Waste tracked', 'new_score': new_score}), 201


@main.route('/api/recipes', methods=['POST'])
@login_required
def create_recipe():
    db = current_app.extensions['sqlalchemy'].db
    data = request.json
    new_recipe = Recipe(
        name=data['name'],
        ingredients=data['ingredients'],
        steps=data['steps'],
        user_id=current_user.id
    )
    db.session.add(new_recipe)
    db.session.commit()
    logging.info({'status': 'Recipe created'}), 201

    # Create response object
    resp = make_response(render_template('recipes.html'))

    return resp, 201


@main.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    logging.info([recipe.serialize() for recipe in recipes]), 200


@main.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_single_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        logging.info({'error': 'Recipe not found'}), 404
    logging.info(recipe.serialize()), 200


@main.route('/secure', methods=['GET'])
@jwt_required()
def secure_route():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)

    if not user:
        logger.warning(f'User not found: {current_user_id}')
        logging.info({'message': 'User not found'}), 404

    logging.info({'message': 'This is a secure route'})


@main.route('/admin', methods=['GET'])
@token_required
def admin_route():
    current_user_id = get_jwt_identity()
    print(current_user_id)
    user = User.find_by_id(current_user_id)

    if not user.has_role('admin'):
        logger.warning(f'Unauthorized access attempt by: {current_user_id}')
        logging.info({'message': 'You do not have permission to access this route'}), 403

    logging.info({'message': 'This is an admin route'})


@main.route('/change_password', methods=['POST'])
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

        # Additional code for invalidating JWT tokens goes here

        return jsonify({'message': 'Password changed successfully'}), 200
    else:
        logging.error(f'Failed to change password for user: {current_user_id}')
        return jsonify({'message': 'Could not change password'}), 500


@main.route('/admin')
@admin_permission.require(http_exception=403)
def admin():
    return 'Admin page'


@main.route('/some_path')
@limiter.limit("5 per minute")  # Override the default rate limit for this route
def some_route():
    return 'This is some route.'


@main.route('/offer/<int:offer_id>')
def show_offer(offer_id):
    offer = get_offer(offer_id)
    logging.info(offer)


@main.route('/api/search_recipes', methods=['GET'])
def search_recipes():
    db = current_app.extensions['sqlalchemy'].db
    query = db.session.query(Recipe)

    # Filtering by dietary restrictions
    dietary_restrictions = request.args.get('dietary_restrictions')
    if dietary_restrictions:
        query = query.filter(Recipe.dietary_restrictions.ilike(f"%{dietary_restrictions}%"))

    # Filtering by cuisine type
    cuisine_type = request.args.get('cuisine_type')
    if cuisine_type:
        query = query.filter(Recipe.cuisine_type == cuisine_type)

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

    recipes = query.all()
    logging.info([recipe.serialize() for recipe in recipes])


@main.route('/offer/update/<int:offer_id>', methods=['POST'])
def update_offer(offer_id):
    # ... update offer logic ...
    invalidate_offer_cache(offer_id)
    logging.info({"status": "Offer updated and cache invalidated."})


@main.route('/api/meal_plan', methods=['POST'])
@login_required
def create_meal_plan():
    db = current_app.extensions['sqlalchemy'].db
    recipe_ids = request.json['recipe_ids']
    new_plan = MealPlan(user_id=current_user.id, recipe_ids=recipe_ids)
    db.session.add(new_plan)
    db.session.commit()
    logging.info({'status': 'Meal plan created'}), 201

    # Create response object
    resp = make_response(render_template('meal_plans.html'))

    return resp, 201


@main.route('/api/meal_plan', methods=['GET'])
@login_required
def get_meal_plans():
    plans = MealPlan.query.filter_by(user_id=current_user.id).all()
    logging.info([plan.serialize() for plan in plans]), 200


@main.route('/grocery-lists', methods=['GET', 'POST'])
@login_required
def handle_grocery_lists():
    db = current_app.extensions['sqlalchemy'].db
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        items = data.get('items')

        # Validation
        if not name or not items:
            return jsonify({"error": "Name and items are required"}), 400

        # Create a new GroceryList object and save it to the database
        new_grocery_list = GroceryList(name=name, items=items, user_id=current_user.id)
        db.session.add(new_grocery_list)
        db.session.commit()

        return jsonify({"message": "Grocery list created successfully"}), 201

    elif request.method == 'GET':
        # Fetch all grocery lists for the current user from the database
        grocery_lists = GroceryList.query.filter_by(user_id=current_user.id).all()

        # Prepare the output
        output = []
        for grocery_list in grocery_lists:
            list_data = {}
            list_data['id'] = grocery_list.id
            list_data['name'] = grocery_list.name
            list_data['items'] = grocery_list.items
            output.append(list_data)

        return jsonify({"grocery_lists": output}), 200


@main.route('/search-grocery-lists', methods=['GET'])
def search_grocery_lists():
    query = request.args.get('query')
    grocery_lists = GroceryList.query.filter(GroceryList.name.like(f"%{query}%")).all()
    return jsonify([grocery_list.serialize() for grocery_list in grocery_lists])


@main.route('/api/update_profile', methods=['POST'])
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


@main.route('/api/fridge/bulk_add', methods=['POST'])
@login_required
def bulk_add_items():
    items = request.json.get('items', [])
    if not items:
        return jsonify({'error': 'No items provided'}), 400

    for item in items:
        # Validate item fields here
        new_item = Product(
            name=item['name'],
            expiration_date=item['expiration_date'],
            weight=item.get('weight', None),
            category=item.get('category', None),
            unit=item.get('unit', None),
            user_id=current_user.id
        )
        db.session.add(new_item)
    db.session.commit()
    return jsonify({'status': 'Items added'}), 201


@main.route('/api/fridge/bulk_remove', methods=['POST'])
@login_required
def bulk_remove_items():
    db = current_app.extensions['sqlalchemy'].db
    item_ids = request.json['item_ids']
    Product.query.filter(Product.id.in_(item_ids)).delete(synchronize_session='fetch')
    db.session.commit()
    logging.info({'status': 'Items removed'}), 200
    return render_template('login.html')


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


@main.errorhandler(400)
def handle_400(error):
    logging.info({f'{error}': 'Bad Request'}), 400


@main.errorhandler(401)
def handle_401(error):
    logging.info({f'{error}': 'Unauthorized'}), 401


@main.errorhandler(404)
def handle_404(error):
    logger.warning('404 error occurred')
    logging.info({f'{error}': 'Resource not found}'}), 404


@main.errorhandler(500)
def handle_500(error):
    logger.critical('500 error occurred', exc_info=True)
    logging.info({f'{error}': 'An internal error occurred'}), 500
