import dash
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask_server import User
import logging


def login_callbacks():
    @dash.callback(
        [Output("login-alert", "is_open"),
         Output("login-name", "value"),
         Output("login-password", "value"),
         Output("login-url", "pathname")],
        Input("id-login-btn", "n_clicks"),
        [State("login-name", "value"),
         State("login-password", "value"),
         State("login-alert", "is_open")],
        prevent_initial_call=True
    )
    def login(login_clicks, username, password, is_open):
        if not login_clicks:
            raise PreventUpdate  # 如果没有点击按钮，避免不必要的更新

        if not username or not password:
            logging.info("用户名或密码为空")
            return not is_open, None, None, None, "/dash/login"  # 如果用户名或密码为空，直接返回 None

        # 根据用户名查询数据库
        user = User.query.filter_by(username=username).first()
        logging.info(f'判断用户存在 {user}')
        if user and check_password_hash(user.hash_password, password):  # 用户存在
            login_user(user, remember=True)
            logging.info("用户登录成功")
            return is_open, username, password, "/dash/nodebb"
        return not is_open, None, None, None, "/dash/login"
