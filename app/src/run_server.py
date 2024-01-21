from app import app

from auth import auth_app
from product_routes import product_app
from order_routes import order_app

if __name__ == '__main__':
    app.register_blueprint(auth_app)
    app.register_blueprint(product_app)
    app.register_blueprint(order_app)

    app.run(host='0.0.0.0', port=8000, debug=True)