import psycopg2
from flask import current_app

from config import db_config
from product import get_product_by_name_with_cursor


class InvalidProduct(Exception):
    pass


class ProductOutOfStock(Exception):
    pass


class Order:
    
    def __init__(self, id, user_id, product_ids_and_quantities):
        self.id = id
        self.user_id = user_id
        self.product_ids_and_quantities = product_ids_and_quantities
    
    def __repr__(self):
        return f'Order[id={self.id}][user_id={self.user_id}][product_list={self.product_ids_and_quantities}]'
    
    @staticmethod
    def create_order(user_id, product_names_and_quantities):
        connection = psycopg2.connect(**db_config)
        with connection:
            with connection.cursor() as cursor:

                order_items = []
                for product_name, order_quantity in product_names_and_quantities:
                    product = get_product_by_name_with_cursor(cursor, product_name)
                    if product is None:
                        connection.rollback()
                        raise InvalidProduct
                    elif product.stock < order_quantity:
                        connection.rollback()
                        raise ProductOutOfStock
                    
                    product.stock -= order_quantity
                    product.update_to_db_with_cursor(cursor)
                    
                    order_items.append((product.id, order_quantity))

                order_id = Order.insert_order_to_db(cursor, user_id)
                Order.insert_order_items_to_db(cursor, order_id, order_items)

                connection.commit()

        return
    
    @staticmethod
    def insert_order_to_db(cursor, user_id):
        cursor.execute("""
            INSERT INTO orders
            (user_id)
            VALUES
            (%s)
            RETURNING id
        """, 
        (user_id,))
        
        return cursor.fetchone()[0]
    
    @staticmethod
    def insert_order_items_to_db(cursor, order_id, order_items):
        for product_id, order_quantity in order_items:    
            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, quantity)
                VALUES
                (%s, %s, %s)
            """,
        (order_id, product_id, order_quantity))