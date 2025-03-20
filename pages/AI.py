import dash
from dash import html


dash.register_page(__name__, path="/AI")  # 使用 `dash.pages`


# AI模型
layout = html.Div([
    html.P("接入大模型接口")
])


