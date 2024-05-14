from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager




app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# login_parent = LoginManager(app)

# hàm hiển thị cho quá trình đăng nhập
login.login_view = 'login'
# login_parent.login_parent_view = 'login_parent'


from app import routes, models