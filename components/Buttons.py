from dash import html
import dash_bootstrap_components as dbc


def home_login_button():
    return html.Div([
        dbc.Button("登录", id="home-login-btn", href="/dash/login", color="primary"),
    ])


def add_contacts_button():
    return html.Div([
        dbc.Button(
            "添加联系人",
            id="add-button",
            color="primary",
            n_clicks=0,

        )
    ], style={
        'color': 'white',  # 按钮文字颜色
        'border': 'none',
        'borderRadius': '5px',
        'padding': '10px 20px',
        'fontSize': '14px',
    },
    )


def delete_contacts_button():
    return html.Div([
        dbc.Button(
            "删除联系人",
            id="delete-button",
            color="primary",
            n_clicks=0,

        )
    ], style={
        # 'position': 'absolute',
        # 'top': '10px',
        # 'right': '10px',
        # 'z-index': '10',
        # 'backgroundColor': '#007bff',  # 按钮背景色
        'color': 'white',  # 按钮文字颜色
        'border': 'none',
        'borderRadius': '5px',
        'padding': '10px 20px',
        'fontSize': '14px',
    },
    )

