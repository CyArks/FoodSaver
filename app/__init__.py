from flask_jwt_extended import JWTManager

from config import DevelopmentConfig, ProductionConfig
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from app.routes import main
import logging
import os


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['JWT_TOKEN_LOCATION'] = ['headers']  # This is the missing configuration

    jwt = JWTManager(app)

    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    # ... rest of your create_app function ...

    app.register_blueprint(main)
    # Initialize other extensions'
    # db.init_app(app)
    # login_manager.init_app(app)

    # Configure logging
    handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # Error Handling
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({f"{error}": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({f"{error}": "Internal Server Error"}), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
