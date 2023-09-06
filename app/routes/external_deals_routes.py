import logging
import requests
from flask import Blueprint
from app.HelperFunctions.cache_manager import get_offer, invalidate_offer_cache
from flask_login import login_required, current_user

deals_blueprint = Blueprint('deals', __name__)


@deals_blueprint.route('/api/fetch_deals', methods=['GET'])
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


@deals_blueprint.route('/offer/<int:offer_id>')
def show_offer(offer_id):
    offer = get_offer(offer_id)
    logging.info(offer)


@deals_blueprint.route('/offer/update/<int:offer_id>', methods=['POST'])
def update_offer(offer_id):
    # ... update offer logic ...
    invalidate_offer_cache(offer_id)
    logging.info({"status": "Offer updated and cache invalidated."})
