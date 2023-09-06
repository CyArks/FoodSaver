import logging

from flask import Blueprint, make_response, render_template, current_app, request
from flask_login import login_required, current_user

from app.Models.RecipeModel import MealPlan

meal_plans_blueprint = Blueprint('meal_plans', __name__)


@meal_plans_blueprint.route('/api/create_meal_plan', methods=['POST'])
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


@meal_plans_blueprint.route('/api/meal_plan', methods=['GET'])
@login_required
def get_meal_plans():
    plans = MealPlan.query.filter_by(user_id=current_user.id).all()
    logging.info([plan.serialize() for plan in plans])

    resp = make_response(render_template('meal_plans.html'))

    return resp, 200

