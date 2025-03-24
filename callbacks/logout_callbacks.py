import dash
from dash import Input, Output
from flask_login import logout_user, current_user
from dash.exceptions import PreventUpdate
import logging


def logout_callbacks():
    @dash.callback(
        Output('url', 'pathname'),
        Input('user-logout-btn', 'n_clicks'),
        prevent_initial_call=True  # 防止初始时执行
    )
    def logout(n_clicks):
        if not n_clicks:
            raise PreventUpdate  # 如果没有点击按钮，避免不必要的更新

        if n_clicks > 0:
            logging.info("点击登出")
            logout_user()  # 使用flask-login的登出方法
            logging.info("登出成功", current_user.is_authenticated)
            return "/dash/home"