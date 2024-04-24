import logging
from flask import Blueprint, request, render_template, jsonify
from flask_login import login_required, current_user
from app.Models.init_alchemy_database import db
from app.Models.ProductModel import Product

stored_products_blueprint = Blueprint('fridge', __name__)


@stored_products_blueprint.route('/api/fridge/bulk_add', methods=['POST'])
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


@stored_products_blueprint.route('/api/fridge/bulk_remove', methods=['POST'])
@login_required
def bulk_remove_items():
    item_ids = request.json['item_ids']
    Product.query.filter(Product.id.in_(item_ids)).delete(synchronize_session='fetch')
    db.session.commit()
    logging.info({'status': 'Items removed'}), 200
    return render_template('login.html')
