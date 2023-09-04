from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from app.routes import auth_blueprint, deals_blueprint, recipes_blueprint, grocery_lists_blueprint, \
    waste_tracking_blueprint, meal_plans_blueprint, profile_blueprint, fridge_blueprint, registration_blueprint, \
    error_handling_blueprint
from app.routes import main
from models import db, User
from flask_caching import Cache
import logging
import os


# Initialize extensions
jwt = JWTManager()
cache = Cache()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)
        # import pdb
        # pdb.set_trace()

    jwt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(deals_blueprint)
    app.register_blueprint(waste_tracking_blueprint)
    app.register_blueprint(recipes_blueprint)
    app.register_blueprint(meal_plans_blueprint)
    app.register_blueprint(grocery_lists_blueprint)
    app.register_blueprint(fridge_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(registration_blueprint)
    app.register_blueprint(error_handling_blueprint)

    # Initialize other extensions'
    with app.app_context():
        db.create_all()

    # Configure logging
    handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error Handling
    @app.errorhandler(403)
    def forbidden_error(error):
        logging.error(error)
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(404)
    def not_found_error(error):
        logging.error(error)
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logging.error(error)
        return jsonify({f"error": "Internal Server Error"}), 500

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5001, debug=True)
