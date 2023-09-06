from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_migrate import Migrate
from config import DevelopmentConfig, ProductionConfig
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from app.routes import recipes_routes, main_routes, auth_routes, user_routes, user_product_routes, \
    error_handling_routes, external_deals_routes, grocery_list_routes, meal_planer_routes, settings_routes, \
    waste_tracking_routes
from app.routes.main_routes import main
from app.Models.UserModel import User
from flask_caching import Cache
from app.Models.init_alchemy_database import db
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

    # Register blueprints with url_prefix
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth_routes.auth_blueprint, url_prefix='/auth')
    app.register_blueprint(external_deals_routes.deals_blueprint, url_prefix='/deals')
    app.register_blueprint(waste_tracking_routes.waste_tracking_blueprint, url_prefix='/waste-tracking')
    app.register_blueprint(recipes_routes.recipes_blueprint, url_prefix='/recipes')
    app.register_blueprint(meal_planer_routes.meal_plans_blueprint, url_prefix='/meal-plans')
    app.register_blueprint(grocery_list_routes.grocery_lists_blueprint, url_prefix='/grocery-lists')
    app.register_blueprint(user_product_routes.stored_products_blueprint, url_prefix='/stored-products')
    app.register_blueprint(user_routes.profile_blueprint, url_prefix='/profile')
    app.register_blueprint(error_handling_routes.error_handling_blueprint, url_prefix='/error-handling')
    app.register_blueprint(settings_routes.settings_blueprint, url_prefix='/settings')

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
