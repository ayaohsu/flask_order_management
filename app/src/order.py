import psycopg2

from config import db_config
from product import Product


class InvalidProduct(Exception):
    pass


class ProductOutOfStock(Exception):
    pass


class Order:
    
    def __init__(self, id, user_id, order_items):
        self.id = id
        self.user_id = user_id
        self.order_items = order_items
    
    def __repr__(self):
        return f'Order[id={self.id}][user_id={self.user_id}][product_list={self.order_items}]'
    
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'products': [{
                'name': item[0],
                'quantity': item[1]
            } for item in self.order_items]
        }
    
    @staticmethod
    def create_order(user_id, product_names_and_quantities):
        connection = psycopg2.connect(**db_config)
        with connection:
            with connection.cursor() as cursor:

                order_items = []
                for product_name, order_quantity in product_names_and_quantities:
                    product = Product.get_product_by_name_with_cursor(cursor, product_name)
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
        cursor.execute('''
            INSERT INTO orders
            (user_id)
            VALUES
            (%s)
            RETURNING id
        ''', 
        (user_id,))
        
        return cursor.fetchone()[0]
    
    @staticmethod
    def insert_order_items_to_db(cursor, order_id, order_items):
        for product_id, order_quantity in order_items:    
            cursor.execute('''
                INSERT INTO order_items
                (order_id, product_id, quantity)
                VALUES
                (%s, %s, %s)
            ''',
        (order_id, product_id, order_quantity))
            
    @staticmethod
    def get_orders(user_id=None):
        connection = psycopg2.connect(**db_config)
        order_list = []

        with connection:
            with connection.cursor() as cursor:
                if (user_id is not None):
                    cursor.execute('''
                        SELECT id, user_id
                        FROM orders
                        WHERE user_id=%s
                    ''',
                    (user_id))
                else:
                    cursor.execute('''
                        SELECT id, user_id
                        FROM orders
                    ''')
                
                order_records = cursor.fetchall()

                
                for order_record in order_records:
                    order_id = order_record[0]
                    order_user_id = order_record[1]

                    cursor.execute('''
                        SELECT p.name, quantity
                        FROM order_items i, products p
                        WHERE i.product_id = p.id
                        AND order_id = %s
                    ''',
                    (order_id,))

                    order_items = cursor.fetchall()
                    order = Order(order_id, order_user_id, order_items)
                    order_list.append(order)
                
                connection.commit()

        return order_list