import logging
from flask_login import login_required, current_user
from flask import Blueprint, current_app, request
from jsonschema.validators import validate
from marshmallow import ValidationError

from app.Models.UserModel import WasteTracking

waste_tracking_blueprint = Blueprint('waste_tracking', __name__)

waste_schema = {
    "type": "object",
    "properties": {
        "food_item_id": {"type": "string"},
        "action": {"type": "string", "enum": ["Used", "Thrown"]},
    },
    "required": ["food_item_id", "action"]
}


@waste_tracking_blueprint.route('/api/track_waste', methods=['POST'])
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
