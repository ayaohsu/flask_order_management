# Online Test - Product and Order Management Service

### Tech Stack

This is an implementation of a product and order management service, using Flask and PostgreSQL, containerized by Docker.

I chose to use a SQL database (RDBMS) since we are mostly dealing with structured data here (like products and orders). Also RDBMS supoprts integrity constraints so some of the checks can be implemented in the db level instead of needing to be addded in the application code.

### To Run the Service

1. Clone the git repo to your local machine and make sure docker environment is set up

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

5. I used a Postman client to send requests to the service. Please use these following credentials to log into and test the service:

| Username    | Password |  Role  |
| -------- | ------- | ------- |
| manager01  | p@ss    | Manager  |
| customer01  | w0rd    | Customer  |

### REST API Endpoints

| Method    | URI |  Request Parameters  |
| -------- | ------- | ------- |
| POST  | `/login`    | fields: `username`, `password` (form-data)   |
| POST  | `/logout`    |   |
| POST  | `/create_product`    | fields: `name`, `price`, `stock` (form-data) |
| PUT  | `/edit_product`    | fields: `name`, `price`, `stock` (form-data) |
| DELETE  | `/delete_product`    | fields: `name` (form-data) |
| GET  | `/product_list`    | fields (all are optional): `min-price`, `max-price`, `min-stock`, `max-stock` (query params)  |
| POST  | `/create_order`    | key=product-name, value=order-quantity (form-data) |
| GET  | `/order_list`    |  |


### TODO List

The validation of the request parameters is not implemented yet - I haven't found a good way to do this except for manually checking the data type and range. I suspect there should be a library to validate this easily. However, I have yet to find one.

At this time, all requests are simply responded with status codes and messages. I know HTML documents could have been returned so it will be easier to test and play around. Redirecting can also be implemented to make the user experience better, in cases like login failure.

In my opinion it is also a good idea to include some unit tests (perhaps with pytest) and end-to-end tests for real-life scenarios like login / logout, role-based access control, product's full life cycle, etc. 

### Contact

If there is any question, please do not hesitate to contact me.  
Thank you for taking the time to review this!

Yao Hsu  
ayao780607@gmail.com
