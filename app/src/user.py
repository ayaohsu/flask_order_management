from flask_login import UserMixin
import psycopg2

from config import db_config

class User(UserMixin):

    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

    def __repr__(self):
        return f'User[id={self.id}][username={self.username}][password_hash={self.password_hash}][role={self.role}]'


def get_user_by_id(id):
    connection = psycopg2.connect(**db_config)
    
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, username, password_hash, role 
        FROM users
        WHERE id = %s
    ''',
    (id,)
    )

    if cursor.rowcount == 0:
        return None
    
    user_record = cursor.fetchone()
    
    cursor.close()
    connection.close()

    return User(user_record[0], user_record[1], user_record[2], user_record[3])

def get_user_by_username(username):
    connection = psycopg2.connect(**db_config)
    
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, username, password_hash, role 
        FROM users
        WHERE username = %s
    ''',
    (username,)
    )

    if cursor.rowcount == 0:
        return None
    
    user_record = cursor.fetchone()

    cursor.close()
    connection.close()

    return User(user_record[0], user_record[1], user_record[2], user_record[3])