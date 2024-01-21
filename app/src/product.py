from flask import current_app
import psycopg2

from config import db_config

LARGE_ENOUGH_PRICE = 1e+10
LARGE_ENOUGH_STOCK = 1e+10

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
    
    def update_to_db_with_cursor(self, cursor):
        cursor.execute('''
            UPDATE products
            SET
            price=%s,
            stock=%s
            WHERE id=%s
        ''',
        (self.price, self.stock, self.id)
        )

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

def get_product_by_name_with_cursor(cursor, name):
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

def get_products_from_db(query_parameters):
    connection = psycopg2.connect(**db_config)

    cursor = connection.cursor()

    cursor.execute('''
        SELECT id, name, price, stock
        FROM products
        WHERE price >= %(min_price)s AND price <= %(max_price)s
        AND stock >= %(min_stock)s AND stock <= %(max_stock)s
    ''',
    {
        'min_price': float(query_parameters['min_price']) if query_parameters['min_price'] is not None else 0,
        'max_price': float(query_parameters['max_price']) if query_parameters['max_price'] is not None else LARGE_ENOUGH_PRICE,
        'min_stock': int(query_parameters['min_stock']) if query_parameters['min_stock'] is not None else 0,
        'max_stock': int(query_parameters['max_stock']) if query_parameters['max_stock'] is not None else LARGE_ENOUGH_STOCK,
    })
    connection.commit()

    product_records = cursor.fetchall()
    products = []

    for product_record in product_records:
        products.append(Product(*product_record))

    cursor.close()
    connection.close()

    return products