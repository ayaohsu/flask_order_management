from flask import Blueprint, current_app, request, jsonify
from flask_login import login_required, current_user

from auth import role_required
from order import Order, ProductOutOfStock, InvalidProduct
from user import MANAGER_ROLE, CUSTOMER_ROLE


order_app = Blueprint('order_app', __name__)


@order_app.route('/create_order', methods=['POST'])
@login_required
@role_required(CUSTOMER_ROLE)
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
    if current_user.role == MANAGER_ROLE:
        orders = Order.get_orders()
    else:
        orders = Order.get_orders(user_id=current_user.get_id())

    return jsonify([order.serialize() for order in orders]), 200