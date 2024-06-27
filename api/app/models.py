from . import db
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'schema': 'products'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    originalprice = db.Column(db.Integer, nullable=False)
    discountpercentage = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.String(255), nullable=True)
    platform = db.Column(db.String(255), nullable=False)
    productmasterid = db.Column(db.Integer, db.ForeignKey('products.product_master.id'), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)

    product_master = relationship('ProductMaster', back_populates='products')

    def __repr__(self):
        return f'<Product {self.name}>'


class ProductMaster(db.Model):
    __tablename__ = 'product_master'
    __table_args__ = {'schema': 'products'}
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(255), nullable=True)

    products = relationship('Product', back_populates='product_master')
    recommendations = relationship('Recommendation', back_populates='product_master')

    def __repr__(self):
        return f'<ProductMaster {self.name}>'


class Recommendation(db.Model):
    __tablename__ = 'pricerecommendation'
    __table_args__ = {'schema': 'products'}
    productmasterid = db.Column(db.Integer, db.ForeignKey('products.product_master.id'), primary_key=True)
    predicted_price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, primary_key=True)

    product_master = relationship('ProductMaster', back_populates='recommendations')

    def __repr__(self):
        return f'<Recommendation {self.productmasterid}, {self.predicted_price}>'
