from flask import request, jsonify, current_app as app
from .auth import auth
from .models import Product, ProductMaster, Recommendation
from . import db

@app.route('/products', methods=['GET'])
@auth.login_required
def get_products():
    products = Product.query.all()
    products_list = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'originalprice': product.originalprice,
            'discountpercentage': product.discountpercentage,
            'detail': product.detail,
            'platform': product.platform,
            'productmasterid': product.productmasterid,
            'created_date': product.created_date
        } for product in products
    ]
    return jsonify(products_list)

@app.route('/product_master', methods=['GET'])
@auth.login_required
def get_product_master():
    product_masters = ProductMaster.query.all()
    product_masters_list = [
        {
            'id': product_master.id,
            'type': product_master.type,
            'name': product_master.name,
            'detail': product_master.detail
        } for product_master in product_masters
    ]
    return jsonify(product_masters_list)

@app.route('/price_recommendations', methods=['GET'])
@auth.login_required
def get_price_recommendations():
    price_recommendations = PriceRecommendation.query.all()
    price_recommendations_list = [
        {
            'id': price_recommendation.id,
            'price_recommendation': price_recommendation.price_recommendation,
            'predicted_price': price_recommendation.predicted_price,
            'date': price_recommendation.date
        } for price_recommendation in price_recommendations
    ]
    return jsonify(price_recommendations_list)

@app.route('/recommendations', methods=['GET'])
@auth.login_required
def get_recommendations():
    recommendations = Recommendation.query.all()
    recommendations_list = [
        {
            'productmasterid': recommendation.productmasterid,
            'predicted_price': recommendation.predicted_price,
            'date': recommendation.date
        } for recommendation in recommendations
    ]
    return jsonify(recommendations_list)
