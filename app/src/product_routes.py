from flask import Blueprint, current_app, request, jsonify
from flask_login import login_required

from auth import role_required
from product import Product
from user import MANAGER_ROLE


product_app = Blueprint('product_app', __name__)


@product_app.route('/create_product', methods=['POST'])
@login_required
@role_required(MANAGER_ROLE)
def create_product():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    current_app.logger.info(f'Received create product request with [name={name}][price={price}][stock={stock}]')

    if Product.insert_product_to_db(name, price, stock):
        return 'Product created.', 201
    else:
        return 'Failed to create product since it exists already.', 400


@product_app.route('/edit_product', methods=['POST'])
@login_required
@role_required(MANAGER_ROLE)
def edit_product():
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])

    current_app.logger.info(f'Received edit product request with [name={name}][price={price}][stock={stock}]')

    product = Product.get_product_by_name(name)
    if product is None:
        return 'Product does not exist.', 400
    
    product.price = price
    product.stock = stock

    product.update_to_db()
    return 'Product updated.', 200


@product_app.route('/delete_product', methods=['DELETE'])
@login_required
@role_required(MANAGER_ROLE)
def delete_product():
    name = request.form['name']

    current_app.logger.info(f'Received delete product request with [name={name}]')

    Product.delete_product_from_db(name)
    return 'Product deleted.', 200


@product_app.route('/product_list')
def get_product_list():
    products_query_parameters = {
        'min_price': request.args.get('min-price'),
        'max_price': request.args.get('max-price'),
        'min_stock': request.args.get('min-stock'),
        'max_stock': request.args.get('max-stock')
    }

    products = Product.get_products_from_db(products_query_parameters)
    return jsonify([product.serialize() for product in products]), 200