from flask import Flask, request, redirect, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from sqlalchemy import or_
from flask_cors import CORS
from config import Config
import requests
import logging
import jwt
from datetime import datetime, timedelta
import json
from keycloak.keycloak_openid import KeycloakOpenID


logger = logging.getLogger(__name__)


# ============================ 🚀 创建 Flask 应用 ============================
# 创建 共享 Flask 服务器
flask_server = Flask(__name__)

# 确保 Secret Key 正确设置，用于加密 session
flask_server.config['SECRET_KEY'] = Config.FLASK_SECRET_KEY
flask_server.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB_WEB}"
flask_server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
flask_server.config['SESSION_COOKIE_SECURE'] = True  # 如果使用 HTTPS，设置为 True
flask_server.config['SESSION_COOKIE_SAMESITE'] = 'None'  # 允许跨域携带 Cookie
flask_server.config['SESSION_COOKIE_DOMAIN'] = '.qiuchengtong.cn'  # 确保跨子域可以共享 cookie


# 配置CORS，允许跨域请求并支持携带Cookie
CORS(flask_server, supports_credentials=True)

# ============================ 配置Flask Login ============================
# 配置 Flask-Login
mysqldb = SQLAlchemy(flask_server)
login_manager = LoginManager()
login_manager.init_app(flask_server)

# ============================ 配置微信登录 ============================
# 微信登录配置参数
APPID = Config.APP_ID  # 替换为你的微信开放平台应用ID
SCOPE = Config.SCOPE  # 请求的权限范围
REDIRECT_URI = Config.ENCODED_REDIRECT_URI  # 登录成功后的回调URL
WECHAT_SECRET = Config.WECHAT_APP_SECRET


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


# ========================== Flask 路由 ===================================
@flask_server.route('/keycloak/callback')
def flask_login():
    code = request.args.get('code')
    logger.info(f"获取keycloak code：{code}")
    token_response = my_keycloak.token(
        grant_type="authorization_code",
        code=code,
        redirect_uri=Config.KEYCLOAK_REDIRECT_URI
    )
    logger.info(f"获取keycloak token：{code}")
    userinfo = my_keycloak.userinfo(token_response['access_token'])
    logger.info(f"获取keycloak userinfo：{userinfo}")
    # 解析用户信息
    # user = json.loads(userinfo)
    username = userinfo['preferred_username']
    email = userinfo['email']
    unionid = userinfo['sub']

    # 根据用户名查询数据库
    # 判断用户是否存在
    user = User.query.filter(or_(User.unionid == unionid, User.email == email)).first()
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
            logger.info("注册keycloak用户: ", username)
            mysqldb.session.add(new_user)
            mysqldb.session.commit()
            logger.info(f"新用户已注册：{username}")
        except Exception as db_error:
            logger.error(f"MySQL数据库错误: {db_error}")
            return 'MySQL数据库错误', 500
    else:
        # 使用 Flask-Login 登录用户
        login_user(user, remember=True)  # 登录用户（此时 user 是 User 模型的实例）, 使用remember参数来设置记住我功能
        logger.info(f'keycloak用户登录成功 {current_user.is_authenticated}')

    return redirect("/")


@flask_server.route('/wechat/callback')
def wechat_callback():
    send_state = session.get('state')
    logger.info(f'发送的 state: {send_state}')
    logger.info("微信授权，返回code和state")
    # 获取微信返回的授权码（code）和防止CSRF攻击的state参数
    code = request.args.get('code')
    logger.info(f'获取微信用户 code: {code}')
    state = request.args.get('state')
    logger.info(f'获取微信用户 state: {state}')

    # 防止 CSRF 攻击，验证 state
    if not code or state != send_state:
        logger.error('验证 state 失败')
        return 'Authorization failed', 400

    try:
        # 使用授权码（code）请求 access_token
        access_token_url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret={WECHAT_SECRET}&code={code}&grant_type=authorization_code'
        logger.info(f'请求用户授权 access_token_url: {access_token_url}')
        access_token_response = requests.get(access_token_url)
        logger.info(f'用户授权响应 access_token_response: {access_token_response}')
        access_token_data = access_token_response.json()
        logger.info(f'获取用户 access_token 及 openid: {access_token_data}')

        # 处理微信 API 错误
        if access_token_response.status_code != 200 or 'access_token' not in access_token_data:
            logger.error(f"获取 access_token 失败: {access_token_data}")
            return '获取 access_token 或 openid 失败', 400

        access_token = access_token_data.get('access_token')
        logger.info(f'用户 access_token: {access_token}')
        openid = access_token_data.get('openid')
        logger.info(f'用户 openid: {openid}')
        refresh_token = access_token_data.get('refresh_token')
        logger.info(f'用户 refresh_token: {refresh_token}')

        if not access_token or not openid:
            logger.error(f"缺失 access token 或 openid")
            return '缺失 access token 或 openid', 400

        # 校验 access_token 是否有效
        valid_url = f'https://api.weixin.qq.com/sns/auth?access_token={access_token}&openid={openid}'
        valid_token_response = requests.get(valid_url)
        valid_token_data = valid_token_response.json()
        valid_status = valid_token_data.get('errmsg')
        logger.info(f'获取验证状态 valid_status:{valid_status}')

        # 获取用户信息
        user_info_url = f'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}'
        user_info_response = requests.get(user_info_url)

        # 使用 response.content 获取字节流，然后解码为字符串
        user_info_content = user_info_response.content.decode('utf-8')

        # 使用 json.loads() 解析 JSON 字符串
        try:
            user_info = json.loads(user_info_content)
        except json.JSONDecodeError as e:
            logger.error(f"解析JSON失败: {e}")
            return '解析JSON失败', 500

        logger.info(f'获取用户信息 user_info:{user_info}')

        username = user_info.get('nickname')
        headimgurl = user_info.get('headimgurl')
        unionid = user_info.get('unionid')

        # 若 access_token 有效
        if valid_status == 'ok':

            # 生成JWT，并将openid存储到cookie中
            payload = {
                "iss": "Socialnet",
                "iat": datetime.utcnow(),
                "exp": datetime.utcnow() + timedelta(days=7),  # 7 天有效期
                "external_id": "dash_wechat_uid_" + str(unionid),
                "username": username,
                "headimgurl": headimgurl,
                "openid": openid,
            }
            jwt_token = jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')
            response = make_response(redirect('/'))  # 登录成功后重定向到主页面
            response.set_cookie('share_auth_token', jwt_token, domain='.qiuchengtong.cn', path='/', secure=True,
                                httponly=True, samesite='None', max_age=60 * 60 * 24 * 7)

            # 判断用户是否存在
            user = User.query.filter_by(open_id=openid).first()  # 根据 openid 查找用户
            logger.info(f'判断微信用户是否存在: {user}')

            if not user:
                logger.info('微信用户不存在，自动注册用户')
                user = User(
                    open_id=openid,
                    username=username,
                    register_type='微信'
                )
                try:
                    logger.info("注册微信用户: ", user_info.get('nickname'))
                    mysqldb.session.add(user)
                    mysqldb.session.commit()
                except Exception as db_error:
                    logger.error(f"MySQL数据库错误: {db_error}")
                    return 'MySQL数据库错误', 500
            else:
                # 使用 Flask-Login 登录用户
                login_user(user, remember=True)  # 登录用户（此时 user 是 User 模型的实例）, 使用remember参数来设置记住我功能
                logger.info(f'微信用户登录成功 {current_user.is_authenticated}')

            return response

        else:
            logger.info(f"access_token 失效: {valid_token_data}")
            return 'access_token 过期', 400

    except Exception as e:
        logging.error(f"微信登陆错误: {e}")
        return f'Internal Server Error: {str(e)}', 500
    finally:
        session.pop('state', None)


@flask_server.route('/logout')
def flask_logout():
    logger.info("Flask 登出路由触发")

    # 使用 flask-login 的登出方法
    logout_user()  # 使用flask-login的登出方法
    logger.info(f"登出成功, 当前用户认证: {current_user.is_authenticated}")

    # 创建响应对象
    response = make_response(redirect('/'))  # 重定向到主页面
    logger.info(f"创建响应对象: {response.status_code}")
    # 删除 'share_auth_token' cookie，设置为过期
    expires = datetime.utcnow() - timedelta(days=1)  # 昨天的时间，使其过期
    logger.info(f"设置过期时间：{expires}")
    logger.info(f"设置 JWT cookie 过期")
    response.set_cookie('share_auth_token', '', expires=expires, path='/', domain='.qiuchengtong.cn', secure=True,
                        httponly=True, samesite='None')

    return response