from flask import Blueprint, current_app, Response, request
from flask_login import login_required
import psycopg2

from config import db_config

product_app = Blueprint('product_app', __name__)

@product_app.route('/create_product', methods=['POST'])
@login_required
def create_product():
    name = request.form['name']
    price = request.form['price']
    stock = request.form['stock']

    current_app.logger.info(f"Received create product request with [name={name}][price={price}][stock={stock}]")
    
    if insert_product_to_db(name, price, stock):
        return Response("Product created.", 201)
    else:
        return Response("Failed to create product since it exists already.", 400)


class Product:

    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f'Product[id={self.id}][name={self.name}][price={self.price}][stock={self.stock}]'

def insert_product_to_db(name, price, stock):
    connection = psycopg2.connect(**db_config)
    
    cursor = connection.cursor()
    query_executed_successfully = True

    try:
        cursor.execute('''
            INSERT INTO products
            (name, price, stock)
            VALUES 
            (%s, %s, %s)
        ''',
        (name, price, stock)
        )
        connection.commit()
    except psycopg2.errors.UniqueViolation:
        current_app.logger.error(f"Attempt to create a product with an existing name. [name={name}]")
        query_executed_successfully = False
    finally:
        cursor.close()
        connection.close()

    return query_executed_successfully