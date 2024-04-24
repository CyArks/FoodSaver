from datetime import datetime
from app.Models.init_alchemy_database import db

# Association table for Recipe and Product (Ingredients)
recipe_product_association \
    = db.Table('recipe_product_association',
               db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id')),
               db.Column('product_id', db.Integer, db.ForeignKey('Product.id'))
               )

# Association table for MealPlan and Recipe
mealplan_recipe_association \
    = db.Table('mealplan_recipe_association',
               db.Column('mealplan_id', db.Integer, db.ForeignKey('MealPlan.id')),
               db.Column('recipe_id', db.Integer, db.ForeignKey('Recipe.id'))
               )


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
