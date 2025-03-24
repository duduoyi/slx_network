import dash
from dash import html


dash.register_page(__name__, path="/kanboard")  # 使用 `dash.pages`


# kanboard
layout = html.Div([
    html.Iframe(
        src="https://www.qiuchengtong.cn/kanboard",  # 这里替换为你想嵌入的网站URL
        width="100%",  # 宽度
        height="600px",  # 高度
        style={"border": "none"}  # 可选的样式，去掉边框
    )
    ], style={
        'display': 'flex',           # 使用Flexbox布局
        'justifyContent': 'center',  # 水平居中
        'alignItems': 'center',      # 垂直居中
        'height': '100vh',           # 设置div的高度为视窗高度的100%，使得它可以垂直居中对齐
        'margin': '0',               # 确保外边距不会影响居中
    }
)
