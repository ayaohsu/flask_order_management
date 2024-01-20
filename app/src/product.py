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


@product_app.route('/edit_product', methods=['POST'])
@login_required
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
def delete_product():
    name = request.form['name']

    current_app.logger.info(f"Received delete product request with [name={name}]")

    if delete_product_from_db(name):
        return Response('Product deleted.', 200)
    else:
        return Response('Failed to delete product.', 500)


class Product:

    def __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock

    def __repr__(self):
        return f'Product[id={self.id}][name={self.name}][price={self.price}][stock={self.stock}]'
    
    def update_to_db(self):
        connection = psycopg2.connect(**db_config)
    
        cursor = connection.cursor()
        query_executed_successfully = True

        try:
            cursor.execute('''
                UPDATE products
                SET
                price=%s,
                stock=%s
                WHERE id=%s
            ''',
            (self.price, self.stock, self.id)
            )
            connection.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to update product to database. [exception={e}][product={self}]")
            query_executed_successfully = False
        finally:
            cursor.close()
            connection.close()
        
        return query_executed_successfully

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

def get_product_by_name(name):
    connection = psycopg2.connect(**db_config)
    
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, name, price, stock 
        FROM products
        WHERE name = %s
    ''',
    (name,)
    )

    if cursor.rowcount == 0:
        return None
    
    product_record = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return Product(product_record[0], product_record[1], product_record[2], product_record[3])

def delete_product_from_db(name):
    connection = psycopg2.connect(**db_config)

    cursor = connection.cursor()
    query_executed_successfully = True

    try:
        cursor.execute('''
            DELETE FROM products
            WHERE name=%s
        ''',
        (name,)
        )
        connection.commit()
    except Exception as e:
        current_app.logger.error(f"Failed to delete product from database. [exception={e}][name={name}]")
        query_executed_successfully = False
    finally:
        cursor.close()
        connection.close()

    return query_executed_successfully