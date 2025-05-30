from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from flask_cors import CORS
from config import Config
import logging
from keycloak.keycloak_openid import KeycloakOpenID
from datetime import datetime
import time
import os

logger = logging.getLogger(__name__)


# 生产环境：设置Unix环境变量, 开发环境：windows开发注释
os.environ['TZ'] = 'Asia/Shanghai'
time.tzset()

# ============================ 🚀 创建 Flask 应用 ============================
# # 创建 共享 Flask 服务器
flask_server = Flask(__name__)

# # 确保 Secret Key 正确设置，用于加密 session
flask_server.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB_WEB}"
# 设置连接超时时间
flask_server.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'connect_timeout': 60},  # 设置连接超时时间为60秒
    'pool_size': 10,  # 设置连接池大小
    'max_overflow': 20,  # 设置连接池的最大溢出量
    'pool_timeout': 30,  # 设置连接池的超时时间
    'pool_recycle': 1800,  # 设置连接池的回收时间
}
flask_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_server.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
flask_server.config['SESSION_COOKIE_NAME'] = 'dash_login'
flask_server.config['SESSION_PERMANENT'] = False  # False 关闭浏览器时，session失效

# 生产环境
flask_server.config['SESSION_COOKIE_SECURE'] = True  # 如果使用 HTTPS，设置为 True
flask_server.config['SESSION_COOKIE_SAMESITE'] = 'None'  # 允许跨域携带 Cookie
flask_server.config['SESSION_COOKIE_DOMAIN'] = '.qiuchengtong.cn'  # 确保跨子域可以共享 cookie

# # 测试环境
# flask_server.config['SESSION_COOKIE_SECURE'] = False  # 如果使用 HTTPS，设置为 True
# flask_server.config['SESSION_COOKIE_SAMESITE'] = 'lax'  # 允许跨域携带 Cookie


# 配置CORS，允许跨域请求并支持携带Cookie
CORS(flask_server, supports_credentials=True)

# ============================ 配置Flask Login ============================
# 配置 Flask-Login
mysqldb = SQLAlchemy(flask_server)
login_manager = LoginManager()
login_manager.init_app(flask_server)

# # ============================ 配置 Keycloak ============================
my_keycloak = KeycloakOpenID(
    server_url=Config.KEYCLOAK_HOST,
    client_id=Config.CLIENT_ID,
    realm_name=Config.REALM_NAME,
    client_secret_key=Config.CLIENT_SECRET_KEY
)

# ============================ 配置 sqlalchemy ============================
# ORM   用户模型
class User(UserMixin, mysqldb.Model):
    __tablename__ = 'users'  # 假设数据库中有一个名为 'users' 的表
    user_id = mysqldb.Column(mysqldb.Integer, primary_key=True)
    username = mysqldb.Column(mysqldb.String(150), unique=True, nullable=False)
    open_id = mysqldb.Column(mysqldb.String(255), nullable=False)
    unionid = mysqldb.Column(mysqldb.String(255), nullable=False)
    email = mysqldb.Column(mysqldb.String(100), nullable=False)
    hash_password = mysqldb.Column(mysqldb.String(255), nullable=False)
    unit = mysqldb.Column(mysqldb.String(100))
    section = mysqldb.Column(mysqldb.String(100))
    user_type = mysqldb.Column(mysqldb.String(50))
    register_type = mysqldb.Column(mysqldb.String(50))
    create_time = mysqldb.Column(mysqldb.DateTime, default=datetime.utcnow)  # 创建时间，默认为当前时间
    update_time = mysqldb.Column(mysqldb.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间，默认为当前时间，更新时自动更新

    def __init__(self, username=None, open_id=None, unionid=None, email=None, hash_password=None, unit=None, section=None, user_type=None, register_type=None):
        self.username = username
        self.open_id = open_id
        self.unionid = unionid
        self.email = email
        self.hash_password = hash_password
        self.unit = unit
        self.section = section
        self.user_type = user_type
        self.register_type = register_type

    def get_id(self):
        return str(self.user_id)  # Flask-Login 需要此方法返回用户唯一标识符

# ========================== Flask-Login 用户加载函数 ===================================
# Flask-Login 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    logger.info(f"加载用户 ID: {user_id}")
    return User.query.get(int(user_id))

# ========================== Flask Login 路由 ===================================
@flask_server.route('/keycloak/callback')
def flask_login():
    code = request.args.get('code')
    logger.info(f"获取keycloak code：{code}")

    try:
        token_response = my_keycloak.token(
            grant_type="authorization_code",
            code=code,
            redirect_uri=Config.KEYCLOAK_REDIRECT_URI
        )
    except Exception as e:
        logger.error(f"获取 keycloak token 错误: {e}")
        return "Error obtaining token from Keycloak", 500

    logger.info(f"获取keycloak token：{token_response}")

    # 获取 token 中的 access_token 和 refresh_token
    access_token = token_response.get('access_token')
    refresh_token = token_response.get('refresh_token')

    # 确保将 access_token 存储在 session 中
    if access_token:
        session['access_token'] = access_token
        logger.info(f"access_token 存入 session：{session.get('access_token')}")
        if refresh_token:
            session['refresh_token'] = refresh_token
            logger.info(f"refresh_token 存入 session：{session.get('refresh_token')}")
    else:
        logger.error("获取的 access_token 为 None")

    try:
        userinfo = my_keycloak.userinfo(token_response['access_token'])
    except Exception as e:
        logger.error(f"获取 userinfo 错误: {e}")
        return "Error fetching userinfo from Keycloak", 500

    logger.info(f"获取keycloak userinfo：{userinfo}")

    # 解析用户信息
    username = userinfo['preferred_username']
    email = userinfo['email']
    unionid = userinfo['sub']

    # 根据用户名查询数据库
    # 判断用户是否存在
    user = User.query.filter(User.email == email).first()
    logger.info(f'判断微信用户是否存在: {user}')

    if not user:
        logger.info("keycloak用户不存在，生成新用户对象")
        new_user = User(
            username=username,
            email=email,
            unionid=unionid,
            register_type='keycloak'
        )
        try:
            logger.info(f"注册keycloak用户: {username}")
            mysqldb.session.add(new_user)
            mysqldb.session.commit()
            logger.info(f"新用户已注册：{username}")
        except Exception as db_error:
            logger.error(f"MySQL数据库错误: {db_error}")
            return 'MySQL数据库错误', 500
    else:
        # 更新用户信息
        logger.info(f"更新keycloak用户: {email}")
        user.username = username
        user.unionid = unionid
        mysqldb.session.commit()
        logger.info(f"用户信息已更新：{username}")
        # 使用 Flask-Login 登录用户
        login_user(user)  # 登录用户（此时 user 是 User 模型的实例）, 使用remember参数来设置记住我功能 , remember=True
        logger.info(f'keycloak用户登录成功 {current_user.is_authenticated}')

    return redirect("/")

# ========================== Flask Logout 路由 ===================================
@flask_server.route('/logout')
def flask_logout():
    logger.info("Flask 登出路由触发")

    refresh_token = session.get('refresh_token')  # 例如您在登录时将 access_token 存入了会话
    logger.info(f"keycloak refresh token: {refresh_token}")

    if refresh_token:
        my_keycloak.logout(refresh_token)
        logger.info(f"keycloak 登出成功")
    else:
        logger.error("没有找到有效的 refresh_token")

    # 使用 flask-login 的登出方法
    logout_user()  # 使用flask-login的登出方法
    logger.info(f"登出成功, 当前用户认证: {current_user.is_authenticated}")

    return redirect("/")