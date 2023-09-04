import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('product', back_populates='user')
    dietary_preference = db.relationship('dietary_preference', backref='owner', lazy='dynamic')
    ratings = db.relationship('ratings', backref='rater', lazy='dynamic')
    meal_plan = db.relationship("meal_plan", backref="user")
    grocery_list = db.relationship("grocery_list", backref="user")
    recipes = db.relationship("recipe", back_populates="user")
    recipe_ratings = db.relationship("recipe_rating", back_populates="user")
    waste_actions = db.relationship("waste_tracking", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        logging.info(f"Password changed/set for user {self.id}.")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        return self.role == role

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", back_populates="products")


class DietaryPreferences(db.Model):
    __tablename__ = 'dietary_preference'
    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.String(64), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Recipes(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(128), index=True)
    ingredients = db.Column(db.String(256))
    ratings = db.relationship('ratings', backref='recipe', lazy='dynamic')


class Ratings(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))


class Notifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class WasteTracking(db.Model):
    __tablename__ = 'waste_tracking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(50), nullable=False)  # Used, Expired, or Thrown
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user = db.relationship("user", back_populates="waste_actions")


class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("user", back_populates="recipes")
    name = db.Column(db.String(64))
    ingredients = db.Column(db.String(512))  # Comma-separated ingredient IDs
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    cuisine_type = db.Column(db.String(64))
    rating = db.Column(db.Float)  # average user rating
    
    # Assuming each recipe can have multiple ratings
    ratings = db.relationship("recipe_rating", back_populates="recipe")


class RecipeRating(db.Model):
    __tablename__ = 'recipe_rating'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))

    user = db.relationship("user", back_populates="recipe_ratings")
    recipe = db.relationship("recipe", back_populates="ratings")


class MealPlan(db.Model):
    __tablename__ = 'meal_plan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_ids = db.Column(db.String(500), nullable=True)  # Comma-separated list of recipe IDs
    date = db.Column(db.DateTime, default=datetime.utcnow)


class GroceryList(db.Model):
    __tablename__ = 'grocery_list'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.String(500), nullable=True)  # Comma-separated list of items
