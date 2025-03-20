import dash
from dash import html
import dash_bootstrap_components as dbc



def network_tabs():
    return html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="现有网络", tab_id="现有网络"),
                dbc.Tab(label="预期网络", tab_id="预期网络"),
            ],
            id="tabs",
            active_tab="现有网络",
        ),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',  # 水平居中
        'alignItems': 'center',  # 垂直居中
        'height': '100%'  # 高度设置为 100% 以便垂直居中
    })


# 测试
if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        network_tabs(),  # 导航栏
    ])
    app.run_server(debug=True)