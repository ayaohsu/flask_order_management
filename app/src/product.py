from flask import Blueprint, current_app, Response, request
from flask_login import login_required

product_app = Blueprint('product_app', __name__)

@product_app.route('/create_product', methods=['POST'])
@login_required
def add_product():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    current_app.logger.info(f"create product with {name}/{price}/{stock}")
    return Response("Product created.", 201)