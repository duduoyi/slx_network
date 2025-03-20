import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from components import Navbar
from flask_server import flask_server
from callbacks import navbar_callbacks, logout_callbacks


# ========== 🏠 创建 Dash 应用 ==========
# 初始化Dash应用
dash_app = dash.Dash(
    __name__,
    server=flask_server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, "https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css"
    ],
    suppress_callback_exceptions=True,
    use_pages=True
)


# ========== 🛠️ Dash 页面布局 ==========
dash_app.layout = html.Div([
    # 顶部导航栏
    Navbar.navbar(),
    dcc.Location(id='url', refresh=True),
    # 主体内容容器（显示 Dash 页面内容）
    html.Div(dash.page_container),
])

navbar_callbacks.navbar_callbacks()
logout_callbacks.logout_callbacks()

# ========== 🚀 开发环境运行应用 ==========
if __name__ == '__main__':
    dash_app.run(debug=True)
