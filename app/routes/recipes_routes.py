import logging
from flask_login import login_required, current_user
from app.Models.RecipeModel import Recipe
from flask import Blueprint, request, render_template, make_response, current_app

recipes_blueprint = Blueprint('recipes', __name__)


@recipes_blueprint.route('/api/create_recipe', methods=['POST'])
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


@recipes_blueprint.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    logging.info([recipe.serialize() for recipe in recipes]), 200


@recipes_blueprint.route('/api/recipes/<int:recipe_id>', methods=['GET'])
def get_single_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe is None:
        logging.info({'error': 'Recipe not found'}), 404
    logging.info(recipe.serialize()), 200


@recipes_blueprint.route('/api/search_recipes', methods=['GET'])
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
