# Online Test - API Implementation of Product and Order Management

### Tech Stack

This is an implementation of a product / order management service, using Flask and PostgreSQL, containerized by Docker.

I chose to use a SQL database (RDBMS) since mostly we are dealing with structured data here (products and orders).

It also comes in handy with integrity constraints that RDBMS provides so less additional check is required at the application level.

### To Run the Service

1. Clone the git repo to your local machine; Ensure docker environment is set up

2. Go to the directory and build the service by running
```
docker compose build
``` 

3. Start the service by running
```
docker compose up -d
```

4. Run the script to create database tables and insert some users into the db (since registration process is not implemented here)

```
cd db
virtualenv venv
pip3 install -r requirements.txt
python init_db.py
```

### REST API Endpoints

| Method    | URI |  Request Parameters  |
| -------- | ------- | ------- |
| POST  | `/login`    | `username`, `password` (form-data)   |
| POST  | `/logout`    |   |
| POST  | `/create_product`    | `name`, `price`, `stock` (form-data) |
| PUT  | `/edit_product`    | `name`, `price`, `stock` (form-data) |
| DELETE  | `/delete_product`    | `name` (form-data) |
| GET  | `/product_list`    | `min-price`, `max-price`, `min-stock`, `max-stock` (Query Params)  |
| POST  | `/create_order`    | <product-name> <order-quantity> (form-data) |
| GET  | `/order_list`    |  |
