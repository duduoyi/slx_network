import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from flask_server import User, mysqldb
import bcrypt
import logging


logger = logging.getLogger(__name__)


dash.register_page(__name__, path="/register")  # 使用 `dash.pages`


# ======================== 用户注册表单 ===========================
logger.info("加载用户注册表单")
user_register_form = html.Div(
    [
        html.H2("欢迎使用三螺旋", className="text-center mb-4"),
        dbc.Alert("密码不一致，请重新确认", id="password-alert", color="danger", is_open=False,
                  className="text-center"),
        dbc.Alert("用户名或密码为空，请重新输入", id="register-alert", color="danger", is_open=False,
                  className="text-center"),
        dbc.Alert("用户名已存在，请重新输入", id="exist-alert", color="danger", is_open=False,
                  className="text-center"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("所属公司",
                                   style={'width': '100px', 'display': 'inline-block', 'textAlign': 'center'}),
                dbc.Input(id="user-unit", type="text", placeholder="请输入公司名称")
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("所属部门",
                                   style={'width': '100px', 'display': 'inline-block', 'textAlign': 'center'}),
                dbc.Input(id="user-section", type="text", placeholder="请输入部门名称")
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("身份类型",
                                   style={'width': '100px', 'display': 'inline-block', 'textAlign': 'center'}),
                dbc.RadioItems(
                    options=[
                        {"label": "老师", "value": "老师"},
                        {"label": "学生", "value": "学生"},
                        {"label": "技术中介", "value": "技术中介"},
                        {"label": "企业人员", "value": "企业人员"},
                        {"label": "政府人员", "value": "政府人员"},
                    ],
                    id="user-type",
                    inline=True,
                    style={
                        "textAlign": "center",  # 保持选项居中
                        "marginLeft": "10px",  # 控制左边距
                        "marginRight": "10px",  # 控制右边距
                        'display': 'flex',  # 使用 flex 布局
                        'alignItems': 'center',  # 垂直居中
                    }
                ),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("用户名",
                                   style={'width': '100px', 'display': 'inline-block', 'textAlign': 'center'}),
                dbc.Input(id="user-name", type="text", placeholder="请输入用户名", required=True)
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("设置密码",
                                   style={'width': '100px', 'display': 'inline-block', 'textAlign': 'center'}),
                dbc.Input(id="set-password", type="password", placeholder="请输入密码", required=True),
                dbc.InputGroupText(
                    html.Img(
                        id="set-password-eye",
                        src="assets/eye-slash.svg",
                        alt="eye",
                        style={"width": "1rem", "height": "1rem"}
                    )
                ),
            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("确认密码",
                                   style={'width': '100px', 'display': 'inline-block', 'textAlign': 'center'}),
                dbc.Input(id="confirm-password", type="password", placeholder="请确认密码", required=True),
                dbc.InputGroupText(
                    html.Img(
                        id="confirm-password-eye",
                        src="assets/eye-slash.svg",
                        alt="eye",
                        style={"width": "1rem", "height": "1rem"}
                    )
                ),
            ],
            className="mb-3",
        ),
        dbc.Row([
            dbc.Button("注册", id="id-register-btn", color="primary", className="d-grid gap-2 mb-3"),
            dbc.Button("已有账号？去登陆", id="go-to-login-btn", href="/login",
                       style={
                           "border": "none",
                           "background": "none",
                           "padding": "0",
                           "color": "#007bff",
                           "marginTop": '15px'
                       })
        ], justify="center", align="center"),
    ],
)


# ==================== 用户注册页 ========================
logger.info("加载用户注册页")
layout = html.Div(
    [
        user_register_form,
        dcc.Location(id='register-url', refresh=True),
    ], style={
        'display': 'flex',  # 使用Flexbox布局
        'justifyContent': 'center',  # 水平居中
        'alignItems': 'center',  # 垂直居中
        'height': '100vh',  # 设置div的高度为视窗高度的100%，使得它可以垂直居中对齐
        'margin': '0',  # 确保外边距不会影响居中
    }
)


# ==================== 用户注册回调函数 ========================
# 设置密码
@dash.callback(
    Output("set-password", "type"),
    Output("set-password-eye", "src"),
    Input("set-password-eye", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_password(n_clicks):
    logger.info("加载设置密码显示隐藏回调函数")
    if n_clicks is None or n_clicks % 2 == 0:
        return "password", "assets/eye-slash.svg"  # 显示眼睛图标
    else:
        return "text", "assets/eye.svg"  # 显示带斜杠的眼睛图标（表示密码已显示）


# 确认密码
@dash.callback(
    Output("confirm-password", "type"),
    Output("confirm-password-eye", "src"),
    Input("confirm-password-eye", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_password(n_clicks):
    logger.info("加载确认密码显示隐藏回调函数")
    if n_clicks is None or n_clicks % 2 == 0:
        return "password", "assets/eye-slash.svg"  # 显示眼睛图标
    else:
        return "text", "assets/eye.svg"  # 显示带斜杠的眼睛图标（表示密码已显示）


# 注册表单
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
    logger.info("加载用户注册回调函数")
    if not n_clicks:
        logger.info("用户未点击按钮")
        raise PreventUpdate  # 如果没有点击按钮，避免不必要的更新

    if con_password != set_password:
        logger.info("密码不一致，重新确认")
        return (not password_alter, register_alter, exist_alter,
                user_unit, user_section, user_type, username, set_password, "", "/register")

    if username is None or set_password is None:
        logger.info("用户名或密码为空，请重新输入")
        return (password_alter, not register_alter, exist_alter,
                user_unit, user_section, user_type, username, set_password, "", "/register")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        logger.info(f'用户: {username} 已存在.')
        return (password_alter, register_alter, not exist_alter,
                user_unit, user_section, user_type, "", "", "", "/register")

    # 加密密码，使用 bcrypt
    hashed_password = bcrypt.hashpw(set_password.encode('utf-8'), bcrypt.gensalt())

    logger.info("生成新用户对象")
    new_user = User(
        username=username,
        hash_password=hashed_password.decode('utf-8'),  # 保存哈希后的密码
        unit=user_unit,
        section=user_section,
        user_type=user_type,
        register_type='账号'
    )
    logger.info("新用户写入数据库")
    mysqldb.session.add(new_user)
    mysqldb.session.commit()
    logger.info(f"新用户已注册：{username}")
    return (password_alter, register_alter, exist_alter,
            user_unit, user_section, user_type, username, set_password, con_password, "/login")
