from flask import Flask
from flask_login import LoginManager, login_user, logout_user, login_required

from user import User, get_user_by_id

app = Flask("OrderNamagement")
app.secret_key = b'ae7566d003089e4107579c96077a20855827a3fa47f27733e0d1088afea8fd48'
login_manager = LoginManager()

@app.route('/')
def hello():
	return "Hello World!"

@app.route('/login', methods=['POST'])
def login():

    user = User(1)
    login_user(user)
    app.logger.info(f'User logs in successfully [user={user}]')
    
    return "Success", 201

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    
    return "Success", 201

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    app.logger.info('Placing order')
    return "Success", 201

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(1)

if __name__ == '__main__':
    login_manager.init_app(app)
    app.run(host='0.0.0.0', port=8000, debug=True)