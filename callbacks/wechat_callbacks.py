import dash
from dash import Input, Output
from flask import session
from flask_server import APPID, REDIRECT_URI, SCOPE
import uuid


def wechat_url_callbacks():
    @dash.callback(
        Output('wechat-url', 'href'),
        Input('wechat-login-btn', 'n_clicks'),
    )
    def trigger_wechat_login(n_clicks):
        if n_clicks is not None:
            # 生成随机的 state 值
            state = str(uuid.uuid4())
            session['state'] = state  # 保存到 session 中

            # 构造微信授权 URL
            wechat_auth_url = f"https://open.weixin.qq.com/connect/qrconnect?appid={APPID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&state={state}#wechat_redirect"
            return wechat_auth_url
        return None