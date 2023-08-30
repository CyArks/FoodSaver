from flask import Flask, jsonify
import logging
from logging.handlers import RotatingFileHandler
from utils.logger import setup_logger
import os
from config import DevelopmentConfig, ProductionConfig


def create_app():
    app = Flask(__name__)
    setup_logger(app)
    
    # Load configurations based on the environment
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize other extensions, routes, etc.

    # Configure logging
    handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Error Handling
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal Server Error"}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
