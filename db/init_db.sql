CREATE TABLE users (
    id VARCHAR ( 10 ) PRIMARY KEY,
    username VARCHAR ( 20 ) NOT NULL,
    password_hash VARCHAR ( 100 ) NOT NULL,
    role VARCHAR ( 15 ) NOT NULL
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR ( 50 ) UNIQUE NOT NULL,
    price NUMERIC NOT NULL,
    stock INTEGER NOT NULL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR ( 10 ) REFERENCES users (id) NOT NULL,
    created_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders (id),
    product_id INTEGER REFERENCES products (id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

INSERT INTO users
(id, username, password_hash, role)
VALUES
('1', 'manager01', '$2b$12$PVAArPGy0TlBfpULT5cShO6X4NToEqHU5r44ehPfut8NWQLBqrc0.', 'Manager');

INSERT INTO users 
(id, username, password_hash, role)
VALUES
('2', 'customer01', '$2b$12$PQr/CiKJo8mt8uww4TxXmu1gP6gjPg61oGW81myWtJgVY5QgvKSMe', 'Customer');