from flask import request, Response, Blueprint, current_app
from flask_login import login_user, logout_user, login_required, current_user

from user import get_user_by_id, get_user_by_username
from app import bcrypt, login_manager

auth_app = Blueprint('auth_app', __name__)


@auth_app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = get_user_by_username(username)
    if user is None:
        current_app.logger.info(f'Attempted to login with a non-existing username [username={username}]')
        return Response('Username does not exist', status=400)

    if bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        current_app.logger.info(f'Logged user in successfully [user={user}]')
        return Response('Logged in', status=201)
    else:
         current_app.logger.info(f'Failed to log user in due to incorrect password [username={username}][input_password={password}]')
         return Response('Login failed', status=400)


@auth_app.route('/logout', methods=['POST'])
@login_required
def logout():
    user_id_to_logout = current_user.get_id()
    logout_user()
    current_app.logger.info(f'Logged out user successfully [user_id={user_id_to_logout}]')
    return Response('Logged out', status=200)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)