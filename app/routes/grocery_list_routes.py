from flask import request, jsonify, current_app, Blueprint
from flask_login import login_required, current_user

from app.Models.GroceryListModel import GroceryList

grocery_lists_blueprint = Blueprint('grocery_lists', __name__)


@grocery_lists_blueprint.route('/grocery-lists', methods=['GET', 'POST'])
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
            list_data = {'id': grocery_list.id, 'name': grocery_list.name, 'items': grocery_list.items}
            output.append(list_data)

        return jsonify({"grocery_lists": output}), 200


@grocery_lists_blueprint.route('/search-grocery-lists', methods=['GET'])
def search_grocery_lists():
    query = request.args.get('query')
    grocery_lists = GroceryList.query.filter(GroceryList.name.like(f"%{query}%")).all()
    return jsonify([grocery_list.serialize() for grocery_list in grocery_lists])
