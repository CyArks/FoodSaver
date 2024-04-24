import logging
from flask import Blueprint

# Create Blueprints
error_handling_blueprint = Blueprint('error_handling', __name__)

# Logger setup
logger = logging.getLogger(__name__)


@error_handling_blueprint.errorhandler(400)
def handle_400(error):
    logging.info({f'{error}': 'Bad Request'}), 400


@error_handling_blueprint.errorhandler(401)
def handle_401(error):
    logging.info({f'{error}': 'Unauthorized'}), 401


@error_handling_blueprint.errorhandler(404)
def handle_404(error):
    logger.warning('404 error occurred')
    logging.info({f'{error}': 'Resource not found}'}), 404


@error_handling_blueprint.errorhandler(500)
def handle_500(error):
    logger.critical('500 error occurred', exc_info=True)
    logging.info({f'{error}': 'An internal error occurred'}), 500
