import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
from dash.exceptions import PreventUpdate
from flask_server import flask_server
from flask_login import current_user
import logging
from datetime import datetime
import os


# ====================== 🏠 配置日志 ======================
# 定义日志存放路径
log_directory = "logs"  # 日志文件夹名称
if not os.path.exists(log_directory):  # 如果目录不存在，则创建
    os.makedirs(log_directory, exist_ok=True)

# 动态生成日志文件名，以当天日期命名
log_filename = datetime.now().strftime("app_%Y-%m-%d.log")
log_file_path = os.path.join(log_directory, log_filename)  # 拼接完整的日志文件路径

# 动态生成日志文件名，以当天日期命名
log_filename = datetime.now().strftime("app_%Y-%m-%d.log")

# 配置日志
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=log_file_path,  # 日志文件名
                    filemode='a')       # 追加模式

# 创建一个日志记录器
logger = logging.getLogger(__name__)


# ====================== 🏠 创建 Dash 应用 ======================
# 初始化Dash应用
logger.info("初始化 Dash 应用")
dash_app = dash.Dash(
    __name__,
    server=flask_server,
    external_stylesheets=[
        'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css',   # 国内镜像源
        'https://at.alicdn.com/t/font_367131_xd3dpkl99n.css',  # 阿里巴巴矢量图标库
    ],
    suppress_callback_exceptions=True,
    use_pages=True
)


# ====================== 主应用布局 ======================
# 主应用
logger.info("加载主应用布局")
dash_app.layout = html.Div([
    # 顶部导航栏
    dbc.Navbar(
        dbc.Container(
            [
                # logo
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(src=dash_app.get_asset_url('images/slx-logo.png'), height="30px"), width="auto"
                            ),
                            dbc.Col(
                                dbc.NavbarBrand(
                                    "三螺旋 小世界",
                                    className="ms-2",
                                    style={"fontFamily": "'Poppins', sans-serif"}
                                ), width="auto"
                            ),
                        ],
                        align="center",
                        className="g-0",
                        justify="start",  # 确保内容水平排列
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                # 导航菜单
                html.Div(id="navbar-menu", children=[]),
                # 用户中心
                html.Div(id="navbar-user", children=[]),
            ],
            fluid=True,  # 让导航栏在不同屏幕尺寸下流式布局
        ),
        className="navbar-expand-lg",  # 添加响应式工具类
        style={
            "position": "fixed",  # 固定导航栏位置
            "top": 0,  # 导航栏位于页面顶部
            "width": "100%",  # 宽度占满整个视口宽度
            "zIndex": 1000,  # 确保导航栏在页面其他内容之上
            "boxShadow": "0px 4px 20px rgba(128, 128, 128, 0.3)",  # 更加柔和的底部阴影
            "backgroundColor": "#FFFFFF",  # 设置导航栏背景颜色
            "height": "60px",  # 增加导航栏高度
            "padding": "10px 20px",  # 增加内边距
        },
    ),
    dcc.Location(id='url', refresh=True),
    # 主体内容容器（显示 Dash 页面内容）
    dash.page_container,
])


# ====================== 导航栏回调函数 ======================
# 导航栏回调
@dash.callback(
    Output('navbar-menu', 'children'),
    Output('navbar-user', 'children'),
    Input('url', 'pathname'),
)
def navbar_change(pathname):
    logger.info(f"导航栏回调触发，当前路径：{pathname}")
    if current_user.is_authenticated:
        logger.info(f'用户已登录, 当前用户认证: {current_user.is_authenticated}')
        return (
            html.Div([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("项目管理", href="https://www.qiuchengtong.cn/kanboard")),
                    dbc.NavItem(dbc.NavLink("活动论坛", href="https://www.qiuchengtong.cn/nodebb")),
                ], className="ml-auto", navbar=True)
            ]),
            html.Div([
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("退出登录", id="user-logout-btn"),
                    ],
                    label="个人中心",
                    id="user-menu",
                )
            ])
        )
    logger.info(f'用户未登录')
    return html.Div(), html.Div([dbc.Button("登录", id="navbar-login-btn", href="/login", color="primary")])


# 登出回调
@dash.callback(
    Output('url', 'pathname'),
    Input('user-logout-btn', 'n_clicks'),
    prevent_initial_call=True  # 防止初始时执行
)
def dash_logout(n_clicks):
    logger.info(f"登出回调触发，n_clicks={n_clicks}")
    if n_clicks is None:
        logger.info("n_clicks 是 None，未点击登出按钮")
        raise PreventUpdate  # 如果没有点击按钮，避免不必要的更新

    if n_clicks > 0:
        logger.info("点击登出")
        return "/logout"


# # ========== 🚀 开发环境运行应用 ==========
# if __name__ == '__main__':
#     logger.info("启动 Dash 应用")
#     dash_app.run(debug=True)
