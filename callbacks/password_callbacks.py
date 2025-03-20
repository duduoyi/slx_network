import dash
from dash import Input, Output


def login_password_callbacks():
    @dash.callback(
        Output("login-password", "type"),
        Output("login-password-eye", "className"),
        Input("login-password-eye", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_password(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            return "password", "bi bi-eye-slash"  # 显示眼睛图标
        else:
            return "text", "bi bi-eye"  # 显示带斜杠的眼睛图标（表示密码已显示）


def set_password_callbacks():
    @dash.callback(
        Output("set-password", "type"),
        Output("set-password-eye", "className"),
        Input("set-password-eye", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_password(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            return "password", "bi bi-eye-slash"  # 显示眼睛图标
        else:
            return "text", "bi bi-eye"  # 显示带斜杠的眼睛图标（表示密码已显示）


def confirm_password_callbacks():
    @dash.callback(
        Output("confirm-password", "type"),
        Output("confirm-password-eye", "className"),
        Input("confirm-password-eye", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_password(n_clicks):
        if n_clicks is None or n_clicks % 2 == 0:
            return "password", "bi bi-eye-slash"  # 显示眼睛图标
        else:
            return "text", "bi bi-eye"  # 显示带斜杠的眼睛图标（表示密码已显示）