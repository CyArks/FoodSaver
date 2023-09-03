from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from app.routes import auth_blueprint
from app.routes import main
from models import db
from flask_caching import Cache
from routes import mongo
import logging
import os


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    jwt = JWTManager(app)
    cache = Cache(app)

    db.init_app(app)
    mongo.init_app(app, uri="mongodb://localhost:27017/foodsaver")
    migrate.init_app(app, db)

    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # Register the auth_blueprint

    # Initialize other extensions'
    with app.app_context():
        db.create_all()

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
