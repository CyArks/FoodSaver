import logging


def setup_logger(app):
    # Setup basic logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    )

    # Integrate with Flask
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.logger.handlers.extend(logging.getLogger("gunicorn").handlers)
