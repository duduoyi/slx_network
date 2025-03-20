import dash
from dash import html, dcc
from components import Forms
from callbacks import password_callbacks, register_callbacks


dash.register_page(__name__, path="/register")  # 使用 `dash.pages`


# 用户注册页
layout = html.Div(
    [
        Forms.user_register_form(),
        dcc.Location(id='register-url', refresh=True),
    ], style={
        'display': 'flex',  # 使用Flexbox布局
        'justifyContent': 'center',  # 水平居中
        'alignItems': 'center',  # 垂直居中
        'height': '100vh',  # 设置div的高度为视窗高度的100%，使得它可以垂直居中对齐
        'margin': '0',  # 确保外边距不会影响居中
    }
)


register_callbacks.register_callbacks()
password_callbacks.set_password_callbacks()
password_callbacks.confirm_password_callbacks()
