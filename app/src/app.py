from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.secret_key = b'ae7566d003089e4107579c96077a20855827a3fa47f27733e0d1088afea8fd48'

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)