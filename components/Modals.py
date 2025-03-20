import dash
from dash import html
import dash_bootstrap_components as dbc
from components import Forms


def user_login_modal():
    return dbc.Modal(
        id="user-login-modal",
        is_open=False,  # 初始关闭
        # is_open=True,  # 测试打开
        children=[
            dbc.ModalHeader(),
            dbc.ModalBody(
                Forms.user_login_form()
            ),
            dbc.ModalFooter()
        ],
    )


def user_register_modal():
    return dbc.Modal(
        id="user-register-modal",
        is_open=False,  # 初始关闭
        # is_open=True,  # 测试打开
        children=[
            dbc.ModalHeader(),
            dbc.ModalBody(
                Forms.user_register_form()
            ),
            dbc.ModalFooter()
        ],
    )


def school_contacts_modal():
    return dbc.Modal(
        id='add-school-modal',
        is_open=False,  # 初始为关闭
        # is_open=True,  # 测试开启
        children=[
            dbc.ModalHeader(),
            dbc.ModalBody([
                Forms.school_contacts_form()
            ]),
            dbc.ModalFooter(),
        ],
    )


def local_contacts_modal():
    return dbc.Modal(
        id='add-local-modal',
        is_open=False,  # 初始为关闭
        # is_open=True,  # 测试打开
        children=[
            dbc.ModalHeader(),
            dbc.ModalBody([
                Forms.local_contacts_form()
            ]),
            dbc.ModalFooter(),
        ],
    )


# 测试
if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
    app.layout = html.Div([
        school_contacts_modal(),
    ])
    app.run_server(debug=True)