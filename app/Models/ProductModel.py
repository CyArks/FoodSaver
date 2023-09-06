from app.Models.init_alchemy_database import db
from app.Models.RecipeModel import recipe_product_association

# Association table for GroceryList and Product
grocerylist_product_association \
    = db.Table('grocerylist_product_association',
               db.Column('grocerylist_id', db.Integer, db.ForeignKey('GroceryList.id')),
               db.Column('product_id', db.Integer, db.ForeignKey('Product.id'))
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
