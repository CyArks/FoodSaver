from cachetools import TTLCache, cached
import logging

logger = logging.getLogger(__name__)  # Added for logging
# Setup cache with 1000 item limit and 3 minutes time-to-live (TTL)
offers_cache = TTLCache(maxsize=1000, ttl=180)

@cached(cache=offers_cache)
def get_offer(offer_id):
    """
    Function to get offer details. This function will be cached.
    """
    # Simulated database query
    # offer = database.get_offer(offer_id)
    return {
        "id": offer_id,
        "title": "Sample Offer",
        "description": "This is a sample offer."
    }

def invalidate_offer_cache(offer_id):
    if offer_id in offers_cache:
        del offers_cache[offer_id]
        logger.info(f"Cache invalidated for offer_id: {offer_id}")
