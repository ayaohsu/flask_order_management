from flask import Blueprint, current_app, Response, request
from flask_login import login_required

from auth import role_required
from product import insert_product_to_db, get_product_by_name, delete_product_from_db, get_products_from_db


product_app = Blueprint('product_app', __name__)


@product_app.route('/create_product', methods=['POST'])
@login_required
@role_required('Manager')
def create_product():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    current_app.logger.info(f"Received create product request with [name={name}][price={price}][stock={stock}]")

    if insert_product_to_db(name, price, stock):
        return Response("Product created.", 201)
    else:
        return Response("Failed to create product since it exists already.", 400)


@product_app.route('/edit_product', methods=['POST'])
@login_required
@role_required('Manager')
def edit_product():
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])

    current_app.logger.info(f"Received edit product request with [name={name}][price={price}][stock={stock}]")

    product = get_product_by_name(name)
    if product is None:
        return Response("Product does not exist.", 400)
    
    product.price = price
    product.stock = stock

    if product.update_to_db():
        return Response('Product updated.', 200)
    else:
        return Response('Failed to update product.', 500)


@product_app.route('/product', methods=['DELETE'])
@login_required
@role_required('Manager')
def delete_product():
    name = request.form['name']

    current_app.logger.info(f"Received delete product request with [name={name}]")

    if delete_product_from_db(name):
        return Response('Product deleted.', 200)
    else:
        return Response('Failed to delete product.', 500)

@product_app.route('/product_list')
def get_product_list():
    products_query_parameters = {
        'min_price': request.args.get('min-price'),
        'max_price': request.args.get('max-price'),
        'min_stock': request.args.get('min-stock'),
        'max_stock': request.args.get('max-stock')
    }

    products = get_products_from_db(products_query_parameters)
    product_names = [ product.name for product in products ]
    return product_names, 200