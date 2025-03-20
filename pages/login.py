import dash
from dash import html, dcc
from components import Forms
from callbacks import login_callbacks, password_callbacks

dash.register_page(__name__, path="/login")  # 使用 `dash.pages`


# 登录页
layout = html.Div([
        Forms.user_login_form(),
        dcc.Location(id='login-url', refresh=True),
    ], style={
        'display': 'flex',           # 使用Flexbox布局
        'justifyContent': 'center',  # 水平居中
        'alignItems': 'center',      # 垂直居中
        'height': '100vh',           # 设置div的高度为视窗高度的100%，使得它可以垂直居中对齐
        'margin': '0',               # 确保外边距不会影响居中
    })


login_callbacks.login_callbacks()
password_callbacks.login_password_callbacks()