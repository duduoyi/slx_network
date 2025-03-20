from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from config import Config


# ========== 🚀 创建 Flask 应用 ==========
# 创建 共享 Flask 服务器
flask_server = Flask(__name__)


# 确保 Secret Key 正确设置，用于加密 session
flask_server.config['SECRET_KEY'] = 'your_secret_key'
flask_server.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB_WEB}"
flask_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# 配置 Flask-Login
mysqldb = SQLAlchemy(flask_server)
login_manager = LoginManager()
login_manager.init_app(flask_server)


# 用户模型
class User(UserMixin, mysqldb.Model):
    __tablename__ = 'users'  # 假设数据库中有一个名为 'users' 的表
    user_id = mysqldb.Column(mysqldb.Integer, primary_key=True)
    username = mysqldb.Column(mysqldb.String(150), unique=True, nullable=False)
    hash_password = mysqldb.Column(mysqldb.String(255), nullable=False)
    unit = mysqldb.Column(mysqldb.String(100))
    section = mysqldb.Column(mysqldb.String(100))
    user_type = mysqldb.Column(mysqldb.String(50))

    def __init__(self, username, hash_password, unit, section, user_type):
        self.username = username
        self.hash_password = hash_password
        self.unit = unit
        self.section = section
        self.user_type = user_type

    def get_id(self):
        return str(self.user_id)  # Flask-Login 需要此方法返回用户唯一标识符


# Flask-Login 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))