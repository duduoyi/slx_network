import dash
from dash import html
import dash_bootstrap_components as dbc
from components import DropdownMenu, Buttons
import base64
from flask_login import current_user


def logo():
    with open("assets/slx_logo/slx-logo.png", "rb") as f:
        encoded_logo = base64.b64encode(f.read()).decode('utf-8')
    return html.A(
        dbc.Row(
            [
                dbc.Col(html.Img(src=f"data:image/png;base64,{encoded_logo}", height="30px")),
                dbc.Col(dbc.NavbarBrand("三螺旋 小世界", className="ms-2")),
            ],
            align="center",
            className="g-0",
        ),
        href="/dash/home",
        style={"textDecoration": "none"},
    )


def menu():
    return dbc.Nav([
        dbc.NavItem(dbc.NavLink("项目管理", href="https://www.qiuchengtong.cn/kanboard")),
        dbc.NavItem(dbc.NavLink("活动论坛", href="https://www.qiuchengtong.cn/nodebb")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("面向高校", href="/dash/school_network"),
                dbc.DropdownMenuItem("面向地方", href="/dash/local_network"),
            ],
            nav=True,
            in_navbar=True,
            label="社交网络",
        ),
        dbc.NavItem(dbc.NavLink("AI大模型", href="/dash/AI")),
    ], className="ml-auto", navbar=True)



def navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                # logo
                logo(),
                # 导航菜单
                html.Div(id="navbar-menu", children=[]),
                # 用户中心
                html.Div(id="navbar-user", children=Buttons.home_login_button()),
            ],
            fluid=True,  # 让导航栏在不同屏幕尺寸下流式布局
        ),
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
    )