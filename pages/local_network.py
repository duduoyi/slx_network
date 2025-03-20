import dash
from dash import html


dash.register_page(__name__, path="/local_network")  # 使用 `dash.pages`


# 社交网络-面向地方
layout = html.Div([
    html.P("跳转到地方关系网络")
])
