from flask import Flask, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user
from config import Config
import requests
import logging


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

# 微信登录配置参数
APPID = Config.APP_ID  # 替换为你的微信开放平台应用ID
SCOPE = Config.SCOPE  # 请求的权限范围
REDIRECT_URI = Config.ENCODED_REDIRECT_URI  # 登录成功后的回调URL
WECHAT_SECRET = Config.WECHAT_APP_SECRET


# 用户模型
class User(UserMixin, mysqldb.Model):
    __tablename__ = 'users'  # 假设数据库中有一个名为 'users' 的表
    user_id = mysqldb.Column(mysqldb.Integer, primary_key=True)
    open_id = mysqldb.Column(mysqldb.String(255), nullable=False)
    username = mysqldb.Column(mysqldb.String(150), unique=True, nullable=False)
    hash_password = mysqldb.Column(mysqldb.String(255), nullable=False)
    unit = mysqldb.Column(mysqldb.String(100))
    section = mysqldb.Column(mysqldb.String(100))
    user_type = mysqldb.Column(mysqldb.String(50))
    register_type = mysqldb.Column(mysqldb.String(50))


    def __init__(self, open_id=None, username=None, hash_password=None, unit=None, section=None, user_type=None, register_type=None):
        self.open_id = open_id
        self.username = username
        self.hash_password = hash_password
        self.unit = unit
        self.section = section
        self.user_type = user_type
        self.register_type = register_type


    def get_id(self):
        return str(self.user_id)  # Flask-Login 需要此方法返回用户唯一标识符


# Flask-Login 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@flask_server.route('/dash/')
def home():
    return redirect('/dash/home')


@flask_server.route('/dash/wechat/callback')
def wechat_callback():
    # 获取微信返回的授权码（code）和防止CSRF攻击的state参数
    code = request.args.get('code')
    logging.info(f'获取微信用户code:{code}')
    state = request.args.get('state')
    logging.info(f'获取微信用户state:{state}')

    # 防止 CSRF 攻击，验证 state
    if not code or state != session.get('state'):
        logging.error('验证 state 失败')
        return 'Authorization failed', 400

    session.pop('state', None)

    try:
        # 使用授权码（code）请求 access_token
        access_token_url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret={WECHAT_SECRET}&code={code}&grant_type=authorization_code'
        logging.info(f'请求用户授权 access_token_url:{access_token_url}')
        access_token_response = requests.get(access_token_url)
        logging.info(f'用户授权响应 access_token_response:{access_token_response}')
        access_token_data = access_token_response.json()
        logging.info(f'获取用户access_token及openid:{access_token_data}')

        # 处理微信 API 错误
        if access_token_response.status_code != 200 or 'access_token' not in access_token_data:
            logging.error(f"Failed to get access_token: {access_token_data}")
            return 'Failed to get access token or openid', 400

        access_token = access_token_data.get('access_token')
        logging.info(f'用户access_token:{access_token}')
        openid = access_token_data.get('openid')
        logging.info(f'用户openid:{openid}')
        refresh_token = access_token_data.get('refresh_token')
        logging.info(f'用户refresh_token:{refresh_token}')

        if not access_token or not openid:
            logging.error(f"Failed to get access token or openid: 400")
            return 'Failed to get access token or openid', 400

        # 校验 access_token 是否有效
        valid_url = f'https://api.weixin.qq.com/sns/auth?access_token={access_token}&openid={openid}'
        valid_token_response = requests.get(valid_url)
        valid_token_data = valid_token_response.json()

        valid_status = valid_token_data.get('errmsg')
        logging.info(f'获取验证状态 valid_status:{valid_status}')

        # 若 access_token 有效
        if valid_status == 'ok':
            # 判断用户是否存在
            user = User.query.filter_by(open_id=openid).first()  # 根据 openid 查找用户
            logging.info(f'判断用户存在: {user}')

            if not user:
                logging.info('用户不存在，自动注册用户')
                user_info_url = f'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}'
                user_info_response = requests.get(user_info_url)
                user_info = user_info_response.json()
                logging.info(f'获取用户信息 user_info:{user_info}')
                user = User(
                    open_id=openid,
                    username=user_info.get('nickname'),
                    register_type='微信'
                )
                try:
                    mysqldb.session.add(user)
                    mysqldb.session.commit()
                except Exception as db_error:
                    logging.error(f"Database error: {db_error}")
                    return 'Database error', 500

            # 使用 Flask-Login 登录用户
            login_user(user)  # 登录用户（此时 user 是 User 模型的实例）
            logging.info(f'微信用户登录{current_user.is_authenticated}')
            return redirect('/dash/home')  # 登录成功后重定向到主页面

        else:
            logging.info(f"Invalid access_token: {valid_token_data}")
            return 'Failed to validate access token', 400

            # # access_token 无效，使用 refresh_token 刷新
            # refresh_token_url = f'https://api.weixin.qq.com/sns/oauth2/refresh_token?appid={APPID}&grant_type=refresh_token&refresh_token={refresh_token}'
            # refresh_token_response = requests.get(refresh_token_url)
            # refresh_token_data = refresh_token_response.json()
            # access_token = refresh_token_data.get('access_token')
            # openid = refresh_token_data.get('openid')
            # refresh_token = refresh_token_data.get('refresh_token')
            # 重新校验新的 access_token
            # return redirect('/wechat/callback')

    except Exception as e:
        logging.error(f"Error during WeChat OAuth process: {e}")
        return f'Internal Server Error: {str(e)}', 500