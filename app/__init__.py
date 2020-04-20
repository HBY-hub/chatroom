# coding:utf8
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_socketio import SocketIO
import pymysql
import os

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/chatroom"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@118.126.104.223:3306/chatroom"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'bc6c782da0124119935f4627417ca55'
app.config["REDIS_URL"] = "redis://localhost:6379"
# app.config["REDIS_URL"] = "redis://118.126.104.223:6379"
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/upload/")
app.config["FC_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/upload/users/")
app.debug = True
db = SQLAlchemy(app)
rd = FlaskRedis(app)
socketio = SocketIO(app)

# from app.home import home as home_blueprint
# from app.admin import admin as admin_blueprint
#
# app.register_blueprint(home_blueprint)
# app.register_blueprint(admin_blueprint, url_prefix='/admin')


login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'main.login'

from app.admin import admin as admin_blueprint

app.register_blueprint(admin_blueprint, url_prefix="/admin")
