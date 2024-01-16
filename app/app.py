from flask import Flask, request, Response
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
from flask_bcrypt import Bcrypt

from user import get_user_by_id, get_user_by_username


app = Flask(__name__)
app.secret_key = b'ae7566d003089e4107579c96077a20855827a3fa47f27733e0d1088afea8fd48'

login_manager = LoginManager()
login_manager.init_app(app)

flask_bcrypt = Bcrypt(app)


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = get_user_by_username(username)
    if user is None:
        app.logger.info(f'Attempted to login with a non-existing username [username={username}]')
        return Response('Username does not exist', status=400)

    if flask_bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        app.logger.info(f'Logged user in successfully [user={user}]')
        return Response('Logged in', status=201)
    else:
         app.logger.info(f'Failed to log user in due to incorrect password [username={username}][password={password}]')
         return Response('Login failed', status=400)


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    user_id_to_logout = current_user.get_id()
    logout_user()
    app.logger.info(f'Logged out user successfully [user_id={user_id_to_logout}]')
    return Response('Logged out', status=200)


@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    app.logger.info('Placing order')
    return Response('Success', status=200)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)