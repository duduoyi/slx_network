import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto


def social_graph():
    return html.Div([
        cyto.Cytoscape(
            id='social_graph',
            elements=[],
            layout={'name': 'concentric'},
            style={'width': '100%', 'height': '100%'},
            stylesheet=[
                # 节点样式
                {
                    'selector': 'node',
                    'style': {
                        'content': 'data(name)',  # 使用节点的 name 字段作为内容
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'color': 'black',
                        'fontSize': '14px',
                        'width': 'data(width)',  # 根据度数设置宽度
                        'height': 'data(height), 50px',  # 根据度数设置高度
                        'background-color': 'data(background-color)',
                    }
                },
                # 边样式
                {
                    'selector': 'edge',
                    'style': {
                        'width': 3,
                        'line-color': '#ccc',
                        'target-arrow-color': '#ccc',
                        'target-arrow-shape': 'triangle',
                        'label': 'data(label)',
                    }
                }
            ]
        )
    ], style={
            'position': 'relative',  # 确保内部元素的绝对定位是相对于这个容器的
            # 'border': '2px solid #ccc',  # 添加边框
            'borderRadius': '10px',  # 圆角
            'backgroundColor': '#f0f0f0',  # 背景色
            'height': 'calc(100vh - 40px)',  # 高度占满视口高度
            'width': '100%',
        }
    )


# 测试
if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        social_graph(),
    ])
    app.run_server(debug=True)
