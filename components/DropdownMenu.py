from dash import html
import dash_bootstrap_components as dbc


def user_features():
    return html.Div([
        dbc.DropdownMenu(
            children=[
                # dbc.DropdownMenuItem("个人资料", id="user-info-btn", href="#"),
                # dbc.DropdownMenuItem("设置", id="user-set-btn", href="#"),
                dbc.DropdownMenuItem("退出登录", id="user-logout-btn"),
            ],
            label="个人中心",
            id="user-menu",
        ),
    ])



