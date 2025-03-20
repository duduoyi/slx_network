import dash
from dash import html
import dash_bootstrap_components as dbc
from utils import filter_list_of_form


def user_login_form():
    return html.Div(
        [
            html.H2("欢迎使用三螺旋！", className="text-center mb-4"),
            dbc.Alert("用户不存在或密码错误，请重新输入", id="login-alert", color="danger", is_open=False, className="text-center"),
            dbc.Form([
                # 用户名输入框
                dbc.Input(id="login-name", type="text", placeholder="请输入用户名", required=True, className="mb-3"),
                # 密码输入框
                dbc.InputGroup([
                    dbc.Input(id="login-password", type="password", placeholder="请输入密码", required=True),
                    dbc.InputGroupText(
                        html.I(id="login-password-eye", className="bi bi-eye-slash"),
                    ),
                ], className="mb-3"),
                dbc.Row([
                    dbc.Button("登录", id="id-login-btn", color="primary", className="d-grid gap-2 mb-3"),
                    # dbc.Col(
                    #     html.Div([
                    #         dbc.Button(
                    #             "忘记密码？",
                    #             id="forget-password-btn",
                    #             style={
                    #                 "border": "none",
                    #                 "background": "none",
                    #                 "padding": "0",
                    #                 "color": "gray",
                    #                 "transition": "color 0.3s ease",
                    #             },
                    #         ),
                    #     ], style={"text-align": "left"}),
                    # ),
                    dbc.Col(
                        html.Div([
                            dbc.Button(
                                "新用户账号注册",
                                id="register-btn",
                                href="/dash/register",
                                style={
                                    "border": "none", "background": "none", "padding": "0", "color": "#007bff"
                                },
                            )
                        ], style={"text-align": "right"}),
                    )
                ]),

            ], className="border p-4"),
            # 添加功能后再显示
            html.Hr(),
            html.Div([
                dbc.Row(
                    html.Div("其他方式登录"),
                    justify="center",  # 让"其他方式登录"居中
                ),
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            dbc.Button(
                                "微信扫码登录",
                                id="weixin-login-btn",
                                style={
                                    "border": "none",
                                    "background": "none",
                                    "padding": "0",
                                    "color": "gray",
                                    "transition": "color 0.3s ease",
                                },
                            ),
                        ]),
                    ),
                    # dbc.Col(
                    #     html.Div([
                    #         dbc.Button(
                    #             "钉钉扫码登陆",
                    #             id="dingding-login-btn",
                    #             style={
                    #                 "border": "none",
                    #                 "background": "none",
                    #                 "padding": "0",
                    #                 "color": "gray",
                    #                 "transition": "color 0.3s ease",
                    #             },
                    #         )
                    #     ]),
                    # )
                ], justify="center", align="center"),  # 将按钮行居中
            ], style={
                "display": "flex",  # 使用 flexbox 布局
                "flexDirection": "column",  # 按照垂直方向排列内容
                "alignItems": "center",  # 水平居中
                "justifyContent": "center",  # 垂直居中
                "width": "100%",  # 使内容填满宽度
            })
        ]
    )





def user_register_form():
    return html.Div(
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
                                       style={'width': '100px', 'display': 'inline-block', 'text-align': 'center'}),
                    dbc.Input(id="user-unit", type="text", placeholder="请输入公司名称")
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("所属部门",
                                       style={'width': '100px', 'display': 'inline-block', 'text-align': 'center'}),
                    dbc.Input(id="user-section", type="text", placeholder="请输入部门名称")
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("身份类型",
                                       style={'width': '100px', 'display': 'inline-block', 'text-align': 'center'}),
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
                                       style={'width': '100px', 'display': 'inline-block', 'text-align': 'center'}),
                    dbc.Input(id="user-name", type="text", placeholder="请输入用户名", required=True)
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("设置密码",
                                       style={'width': '100px', 'display': 'inline-block', 'text-align': 'center'}),
                    dbc.Input(id="set-password", type="password", placeholder="请输入密码", required=True),
                    dbc.InputGroupText(
                        html.I(id="set-password-eye", className="bi bi-eye-slash"),
                    ),
                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText("确认密码",
                                       style={'width': '100px', 'display': 'inline-block', 'text-align': 'center'}),
                    dbc.Input(id="confirm-password", type="password", placeholder="请确认密码", required=True),
                    dbc.InputGroupText(
                        html.I(id="confirm-password-eye", className="bi bi-eye-slash"),
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row([
                dbc.Button("注册", id="id-register-btn", color="primary", className="d-grid gap-2 mb-3"),
                dbc.Button("已有账号？去登陆", id="go-to-login-btn", href="/dash/login",
                           style={
                               "border": "none", "background": "none", "padding": "0", "color": "#007bff", 'marginTop': '15px'
                           })
            ], justify="center", align="center"),
        ],
    )


def school_contacts_form():
    school_data = filter_list_of_form.school_list()
    schools = school_data['school'].unique()
    return html.Div([
        html.H6("请填写高校联系人信息", className="text-center mb-4"),
        dbc.Form([
            dbc.Label("学校"),
            dbc.Select(
                id="school-unit-select",
                options=[
                    {'label': school, 'value': school} for school in schools
                ],
                placeholder="请选择联系人所属学校",
            ),
            html.Br(),
            dbc.Label("学院"),
            dbc.Select(
                id="school-section-select",
                placeholder="请选择联系人所属学院",
            ),
            html.Br(),
            dbc.Label("身份"),
            dbc.Select(
                id="school-post-select",
                options=[
                    {'label': '老师', 'value': '老师'},
                    {'label': '学生', 'value': '学生'},
                ],
                placeholder="请选择联系人身份",
            ),
            html.Br(),
            dbc.Label("姓名"),
            dbc.Input(
                id='school-name-input',
                placeholder="请输入联系人姓名",
            ),
            html.Br(),
            dbc.Label("关系类型"),
            dbc.Select(
                id="school-rel-select",
                options=[
                    {'label': '合作关系', 'value': '合作关系'},
                    {'label': '同事关系', 'value': '同事关系'},
                    {'label': '师生关系', 'value': '师生关系'},
                ],
                placeholder="请选择与联系人的关系类型",
            ),
            html.Br(),

        ]),
        html.Div(
            [
                dbc.Button("提交", id="submit-school-button", color="primary")
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-end",
        )
    ])


def local_contacts_form():
    return html.Div([
        html.H6("请填写地方联系人信息", className="text-center mb-4"),
        dbc.Form([
            dbc.Label("联系人类型"),
            dbc.Select(
                id="local-type-select",
                options=[
                    {'label': '企业人员', 'value': '企业人员'},
                    {'label': '政府人员', 'value': '政府人员'},
                    {'label': '技术中介', 'value': '技术中介'},
                ],
                placeholder="请选择联系人类型",
            ),
            html.Br(),
            dbc.Label("单位"),
            dbc.Select(
                id="local-unit-select",
                placeholder="请选择联系人所属单位",
            ),
            html.Br(),
            dbc.Label("部门"),
            dbc.Input(
                id="local-section-input",
                placeholder="请输入联系人所属部门",
            ),
            html.Br(),
            dbc.Label("岗位"),
            dbc.Input(
                id="local-post-input",
                placeholder="请输入联系人所属岗位",
            ),
            html.Br(),
            dbc.Label("姓名"),
            dbc.Input(
                id='local-name-input',
                placeholder="请输入联系人姓名",
            ),
            html.Br(),
            dbc.Label("关系类型"),
            dbc.Select(
                id="local-rel-select",
                options=[
                    {'label': '合作关系', 'value': '合作关系'},
                    {'label': '同事关系', 'value': '同事关系'},
                    {'label': '师生关系', 'value': '师生关系'},
                ],
                placeholder="请选择关系类型",
            ),
            html.Br(),
        ]),
        html.Div(
            [
                dbc.Button("提交", id="submit-local-button", color="primary")
            ],
            className="d-grid gap-2 d-md-flex justify-content-md-end",
        )
    ])


# 测试
if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        user_login_form(),
    ])
    app.run_server(debug=True)