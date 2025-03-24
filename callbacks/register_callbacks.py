import dash
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from werkzeug.security import generate_password_hash
from flask_server import User, mysqldb


def register_callbacks():
    @dash.callback(
        [Output("password-alert", "is_open"),
         Output("register-alert", "is_open"),
         Output("exist-alert", "is_open"),
         Output("user-unit", "value"),
         Output("user-section", "value"),
         Output("user-type", "value"),
         Output("user-name", "value"),
         Output("set-password", "value"),
         Output("confirm-password", "value"),
         Output("register-url", "pathname")],
        Input("id-register-btn", "n_clicks"),
        [State("password-alert", "is_open"),
         State("register-alert", "is_open"),
         State("exist-alert", "is_open"),
         State("user-unit", "value"),
         State("user-section", "value"),
         State("user-type", "value"),
         State("user-name", "value"),
         State("set-password", "value"),
         State("confirm-password", "value")],
        prevent_initial_call=True
    )
    def register(n_clicks, password_alter, register_alter, exist_alter,
                 user_unit, user_section, user_type, username, set_password, con_password):
        if not n_clicks:
            raise PreventUpdate  # 如果没有点击按钮，避免不必要的更新

        if con_password != set_password:
            print("密码不一致，重新确认")
            return (not password_alter, register_alter, exist_alter,
                    user_unit, user_section, user_type, username, set_password, "", "/dash/register")

        if username is None or set_password is None:
            print("用户名或密码为空，请重新输入")
            return (password_alter, not register_alter, exist_alter,
                    user_unit, user_section, user_type, username, set_password, "", "/dash/register")

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            print(f'User with username {username} already exists.')
            return (password_alter, register_alter, not exist_alter,
                    user_unit, user_section, user_type, "", "", "", "/dash/register")

        new_user = User(
            username=username,
            hash_password=generate_password_hash(set_password),
            unit=user_unit,
            section=user_section,
            user_type=user_type,
            register_type='账号'
        )

        mysqldb.session.add(new_user)
        mysqldb.session.commit()
        print(f"用户已注册：{username}")
        return (password_alter, register_alter, exist_alter,
                user_unit, user_section, user_type, username, set_password, con_password, "/dash/login")