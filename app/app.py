from flask import Flask
from flask_login import LoginManager, login_user, login_required
import secrets

from user import User

app = Flask("OrderNamagement")
app.secret_key = secrets.token_hex()
login_manager = LoginManager()

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/login', methods=['POST'])
def login():
    user = User("1", "admin", "apass")
    login_user(user)
    app.logger.info('User logs in successfully')
    return "Success", 201

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    app.logger.info('Placing order')
    return "Success", 201

@login_manager.user_loader
def load_user(user_id):
    return User().get_user_by_id(user_id) # TODO fix here

if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(host='0.0.0.0', port=8000, debug=True)