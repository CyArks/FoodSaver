import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


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


# Association table for GroceryList and Product
grocerylist_product_association = db.Table('grocerylist_product_association',
    db.Column('grocerylist_id', db.Integer, db.ForeignKey('GroceryList.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('Product.id'))
)

# Association table for Recipe and Product (Ingredients)
recipe_product_association = db.Table('recipe_product_association',
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('Product.id'))
)

# Association table for MealPlan and Recipe
mealplan_recipe_association = db.Table('mealplan_recipe_association',
    db.Column('mealplan_id', db.Integer, db.ForeignKey('MealPlan.id')),
    db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id'))
)


class Product(db.Model):
    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    unit = db.Column(db.String(10), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    user = db.relationship("User", back_populates="product")
    grocerylists = db.relationship('GroceryList', secondary=grocerylist_product_association, back_populates='products')
    recipes = db.relationship('Recipe', secondary=recipe_product_association, back_populates='ingredients')


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


class Recipe(db.Model):
    __tablename__ = 'Recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    cuisine_type = db.Column(db.String(64))
    rating = db.Column(db.Float)  # average user rating
    
    # Assuming each recipe can have multiple ratings
    ingredients = db.relationship('Product', secondary=recipe_product_association, back_populates='recipes')
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    ratings = db.relationship("RecipeRating", back_populates="recipe")
    mealplans = db.relationship('MealPlan', secondary=mealplan_recipe_association, back_populates='recipes')
    user = db.relationship("User", back_populates="recipes")


class RecipeRating(db.Model):
    __tablename__ = 'RecipeRating'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float)

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('Recipe.id'))
    user = db.relationship("User", back_populates="recipe_ratings")
    recipe = db.relationship("Recipe", back_populates="ratings")


class MealPlan(db.Model):
    __tablename__ = 'MealPlan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many relationship with Recipe
    recipes = db.relationship('Recipe', secondary=mealplan_recipe_association, back_populates='mealplans')


class GroceryList(db.Model):
    __tablename__ = 'GroceryList'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    # Many-to-many relationship with Product
    products = db.relationship('Product', secondary=grocerylist_product_association, back_populates='grocerylists')

