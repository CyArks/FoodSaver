import logging
from datetime import datetime
from typing import re

from werkzeug.security import generate_password_hash, check_password_hash
from app.Models.init_alchemy_database import db


class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='User')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    product = db.relationship('Product', back_populates='user')
    dietary_preference = db.relationship('DietaryPreference', backref='owner', lazy='dynamic')
    meal_plan = db.relationship("MealPlan", backref="User")
    grocery_list = db.relationship("GroceryList", backref="User")
    recipes = db.relationship("Recipe", back_populates="user")
    recipe_ratings = db.relationship("RecipeRating", back_populates="user")
    waste_actions = db.relationship("WasteTracking", back_populates="user")

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

    @classmethod
    def email_already_exists(cls, email):
        existing_user = cls.query.filter_by(email=email).first()
        return existing_user is not None

    @classmethod
    def username_is_unique(cls, username):
        existing_user = cls.query.filter_by(username=username).first()
        return existing_user is None


class DietaryPreference(db.Model):
    __tablename__ = 'DietaryPreference'
    id = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.String(64), index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


class Notifications(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(256))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))


class WasteTracking(db.Model):
    __tablename__ = 'WasteTracking'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action = db.Column(db.String(50), nullable=False)  # Used, Expired, or Thrown
    date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    food_item_id = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False)
    user = db.relationship("User", back_populates="waste_actions")
