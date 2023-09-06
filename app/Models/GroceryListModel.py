from app.Models.init_alchemy_database import db
from app.Models.ProductModel import grocerylist_product_association


class GroceryList(db.Model):
    __tablename__ = 'GroceryList'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    # Many-to-many relationship with Product
    products = db.relationship('Product', secondary=grocerylist_product_association, back_populates='grocerylists')
