## 使用 keycloak 登录



# import dash
# from dash import html, dcc, Input, Output, State
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# from flask import session
# from flask_login import login_user
# import bcrypt
# from flask_server import APPID, REDIRECT_URI, SCOPE, User, flask_server
# import logging
# import uuid
# from datetime import timedelta
#
#
# logger = logging.getLogger(__name__)
#
#
# dash.register_page(__name__, path="/login")  # 使用 `dash.pages`
#
#
# # ======================== 登录页表单 ===========================
# # 登录表单
# user_login_form = html.Div(
#     [
#         html.H2("欢迎使用三螺旋！", className="text-center mb-4"),
#         dbc.Alert("用户不存在或密码错误，请重新输入", id="login-alert", color="danger", is_open=False,
#                   className="text-center"),
#         dbc.Form([
#             # 用户名输入框
#             dbc.Input(id="login-name", type="text", placeholder="请输入用户名", required=True, className="mb-3"),
#             # 密码输入框
#             dbc.InputGroup([
#                 dbc.Input(id="login-password", type="password", placeholder="请输入密码", required=True),
#                 dbc.InputGroupText(
#                     html.Img(
#                         id="login-password-eye",
#                         src="assets/eye-slash.svg",
#                         alt="eye",
#                         style={"width": "1rem", "height": "1rem"}
#                     )
#                 ),
#             ], className="mb-3"),
#             dbc.Row([
#                 dbc.Button("登录", id="id-login-btn", color="primary", className="d-grid gap-2 mb-3"),
#                 dbc.Col(
#                     html.Div([
#                         dbc.Button(
#                             "新用户账号注册",
#                             id="register-btn",
#                             href="/register",
#                             style={
#                                 "border": "none", "background": "none", "padding": "0", "color": "#007bff"
#                             },
#                         )
#                     ], style={"textAlign": "right"}),
#                 )
#             ]),
#
#         ], className="border p-4"),
#         # 添加功能后再显示
#         html.Hr(),
#         html.Div([
#             dbc.Row(
#                 html.Div("其他方式登录"),
#                 justify="center",  # 让"其他方式登录"居中
#             ),
#             dbc.Row([
#                 dbc.Col(
#                     html.Div([
#                         dbc.Button(
#                             "微信扫码登录",
#                             id="wechat-login-btn",
#                             style={
#                                 "border": "none",
#                                 "background": "none",
#                                 "padding": "0",
#                                 "color": "gray",
#                                 "transition": "color 0.3s ease",
#                             },
#                         ),
#                     ]),
#                 ),
#             ], justify="center", align="center"),  # 将按钮行居中
#         ], style={
#             "display": "flex",  # 使用 flexbox 布局
#             "flexDirection": "column",  # 按照垂直方向排列内容
#             "alignItems": "center",  # 水平居中
#             "justifyContent": "center",  # 垂直居中
#             "width": "100%",  # 使内容填满宽度
#         })
#     ]
# )
#
# # ======================== 登录页布局 ===========================
# # 登录页
# logger.info("加载用户登录界面")
# layout = html.Div([
#         user_login_form,
#         dcc.Location(id='login-url', refresh=True),  # 用于处理页面跳转
#         dcc.Location(id='wechat-url', refresh=True),  # 用于处理页面跳转
#     ], style={
#         'display': 'flex',           # 使用Flexbox布局
#         'justifyContent': 'center',  # 水平居中
#         'alignItems': 'center',      # 垂直居中
#         'height': '100vh',           # 设置div的高度为视窗高度的100%，使得它可以垂直居中对齐
#         'margin': '0',               # 确保外边距不会影响居中
#     })
#
#
# # ======================== 登录页回调函数 ===========================
# # 账号登陆回调
# @dash.callback(
#     [Output("login-alert", "is_open"),
#      Output("login-name", "value"),
#      Output("login-password", "value"),
#      Output("login-url", "pathname")],
#     Input("id-login-btn", "n_clicks"),
#     [State("login-name", "value"),
#      State("login-password", "value"),
#      State("login-alert", "is_open")],
#     prevent_initial_call=True
# )
# def login(login_clicks, username, input_password, is_open):
#     logger.info("账号登陆回调触发")
#     if not login_clicks:
#         logger.info("未点击登录按钮")
#         raise PreventUpdate  # 如果没有点击按钮，避免不必要的更新
#
#     if not username or not input_password:
#         logger.info("登陆失败，用户名或密码为空")
#         return not is_open, None, None, "/login"  # 如果用户名或密码为空，直接返回 None
#
#     # 根据用户名查询数据库
#     user = User.query.filter_by(username=username).first()
#     logger.info(f'判断用户存在 {user}')
#     if user and bcrypt.checkpw(input_password.encode('utf-8'), user.hash_password.encode('utf-8')):  # 用户存在
#         login_user(user, remember=True)
#         logger.info("用户登录成功")
#         return is_open, username, input_password, "/"
#     logger.info("登陆失败，用户名或密码错误")
#     return not is_open, None, None, "/login"
#
#
# # 密码显示/隐藏回调
# @dash.callback(
#     Output("login-password", "type"),
#     Output("login-password-eye", "src"),
#     Input("login-password-eye", "n_clicks"),
#     prevent_initial_call=True,
# )
# def toggle_password(n_clicks):
#     logger.info("密码显示隐藏回调触发")
#     if n_clicks is None or n_clicks % 2 == 0:
#         return "password", "assets/eye-slash.svg"  # 显示眼睛图标
#     else:
#         return "text", "assets/eye.svg"  # 显示带斜杠的眼睛图标（表示密码已显示）
#
#
# # 微信登陆回调
# @dash.callback(
#     Output('wechat-url', 'href'),
#     Input('wechat-login-btn', 'n_clicks'),
#     prevent_initial_call=True,
# )
# def trigger_wechat_login(n_clicks):
#     logger.info("微信登陆回调触发")
#     if n_clicks is not None:
#         # 生成随机的 state 值
#         state = str(uuid.uuid4())
#         session['state'] = state  # 保存到 session 中
#         # session.permanent = True  # 会话 cookie 持久有效，直到过期时间到达
#         # flask_server.permanent_session_lifetime = timedelta(days=7)  # 设置 cookie 的过期时间
#         logger.info(f"生成新的 state: {state} 并存储到 session")
#
#         # 构造微信授权 URL
#         wechat_auth_url = f"https://open.weixin.qq.com/connect/qrconnect?appid={APPID}&redirect_uri={REDIRECT_URI}&response_type=code&scope={SCOPE}&state={state}#wechat_redirect"
#         logger.info(f"跳转微信授权页 {wechat_auth_url}")
#         return wechat_auth_url
#     return None