from flask import Flask
from flask_login import LoginManager

from user import User

app = Flask("OrderNamagement")
login_manager = LoginManager()

@app.route('/')
def hello():
	return "Hello World!"

@login_manager.user_loader
def load_user(user_id):
    return User()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)
	login_manager.init_app(app)