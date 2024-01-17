DROP TABLE users;

CREATE TABLE users (
    id VARCHAR ( 10 ) PRIMARY KEY,
    username VARCHAR ( 20 ) NOT NULL,
    password_hash VARCHAR ( 100 ) NOT NULL,
    role VARCHAR ( 15 ) NOT NULL
);

INSERT INTO users
(id, username, password_hash, role)
VALUES
('1', 'admin01', '$2b$12$PVAArPGy0TlBfpULT5cShO6X4NToEqHU5r44ehPfut8NWQLBqrc0.', 'admin');

INSERT INTO users 
(id, username, password_hash, role)
VALUES
('2', 'customer01', '$2b$12$PQr/CiKJo8mt8uww4TxXmu1gP6gjPg61oGW81myWtJgVY5QgvKSMe', 'customer');