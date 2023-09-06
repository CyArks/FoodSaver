from flask import jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import g
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the Limiter
limiter = Limiter(
    key_func=get_remote_address,  # Use the remote address as the key
    default_limits=["200 per day", "50 per hour"]  # Global rate limit
)


def configure_rate_limits(app):
    """Initialize rate limiting on the given Flask app."""
    limiter.init_app(app)

    @app.after_request
    def inject_x_rate_headers(response):
        """Add rate limiting headers to responses."""
        limit = getattr(g, 'view_rate_limit', None)
        if limit:
            h = response.headers
            h.add('X-RateLimit-Remaining', str(limit.request_remaining))
            h.add('X-RateLimit-Limit', str(limit.request_limit))
            h.add('X-RateLimit-Reset', str(limit.reset))
        return response

    @limiter.request_filter
    def exempt_users():
        """Exempt users from rate limits."""
        return False  # For now, nobody is exempt

    @app.errorhandler(429)
    def ratelimit_error(e):
        logging.warning('Rate limit exceeded')
        return jsonify({'error': 'ratelimit exceeded'}), 429