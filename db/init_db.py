import psycopg2

if __name__ == '__main__':
    connection = psycopg2.connect(
        database='postgres',
        host='localhost',
        user='postgres_user',
        password='postgres_password',
        port='5432'
    )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(open("init_db.sql", "r").read())
            connection.commit()
    
    print('Finished creating db tables and inserting user records.')