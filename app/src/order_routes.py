from flask import Blueprint, current_app, request, jsonify
from flask_login import login_required, current_user

from auth import role_required
from order import Order, ProductOutOfStock, InvalidProduct


order_app = Blueprint('order_app', __name__)


@order_app.route('/create_order', methods=['POST'])
@login_required
@role_required('Customer')
def create_order():
    
    product_names_and_quantities = []
    for entry_name, entry_value in request.form.items():
        product_names_and_quantities.append((entry_name, int(entry_value)))
    
    if len(product_names_and_quantities) == 0:
        return 'Invalid order with no products specified.', 400
    
    current_app.logger.info(f'Received order request. [user={current_user}][products_and_quantities={product_names_and_quantities}]')

    try:
        Order.create_order(current_user.get_id(), product_names_and_quantities)
    except ProductOutOfStock:
        return 'Product is out of stock.', 400
    except InvalidProduct:
        return 'Product does not exist in our inventory.', 400
    except Exception as e:
        current_app.logger.error(f'Failed to create order due to unexpected error. [exception={e}]')
        return 'Failed to create order.', 500
    
    return 'Success', 201

@order_app.route('/order_list')
@login_required
def get_order_list():
    if current_user.role == 'Manager':
        orders = Order.get_orders()
    elif current_user.role == 'Customer':
        orders = Order.get_orders(user_id=current_user.get_id())
    else:
        current_user.logger.error(f'Got user with unknown role when handling order_list request. [user={current_user}]')
        return 'Failed to get order list.', 500

    return jsonify([order.serialize() for order in orders]), 200