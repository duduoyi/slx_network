import dash
from dash import html, Input, Output
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash.exceptions import PreventUpdate
from data.mysql_connection import MysqlPatent
from data.neo4j_connection import Neo4jConnection
import logging

#
# logger = logging.getLogger(__name__)
#
#
# dash.register_page(__name__, path="/school_network")  # 使用 `dash.pages`

# ======================== mysql 取数 ==============================

mysql_conn = MysqlPatent()
school_college_query = """
        select
            school, college
        from dim_school_college
    """
school_college_df = mysql_conn.get_mysql_data(school_college_query)


# ========================= 筛选栏 ===================================
school_list = school_college_df['school'].unique()

school_filter = html.Div([
    dbc.Select(
        id="school-select",
        options=[{"label": school, "value": school} for school in school_list],
        placeholder='请选择高校',
        className="custom-select",  # 添加自定义样式类
        value="清华大学"
    )
])

college_filter = html.Div([
    dbc.Select(
        id="college-select",
        placeholder='请选择学院',
        className="custom-select",  # 添加自定义样式类
        value="计算机科学与技术系"
    )
])


# 回调函数：学校-学院联动筛选
@dash.callback(
    Output('college-select', 'options'),
    Input('school-select', 'value'),
)
def school_college_filter(school_value):
    if school_value is None:
        raise PreventUpdate

    college_list = school_college_df[school_college_df['school'] == school_value]['college'].unique()
    return [{"label": college, "value": college} for college in college_list]


# ======================== neo4j 取数 ===============================
def school_patent_network(school, college):
    neo4j_conn = Neo4jConnection()
    node_query = f"""
        MATCH (a:`高校人员`)
        WHERE a.unit = '{school}' AND a.section = '{college}' and a.coreValue > 5
        return 
            id(a) as id, 
            a.name AS name, 
            a.unit as unit, 
            a.section as section,
            a.post as post,
            a.weight as weight,
            a.coreValue as coreValue,
            a.communityId as communityId
    """
    logging.info(f"查询高校节点: {node_query}")
    node_data = neo4j_conn.run_query(node_query)

    rel_query = f"""
        MATCH (n:`高校人员`)-[r]-(m:`高校人员`)
        WHERE n.unit = '{school}' AND n.section = '{college}' and n.coreValue > 5
        and m.unit = '{school}' AND m.section = '{college}' and m.coreValue > 5
        return 
            id(n) as source, 
            type(r) AS type,
            id(m) AS target
    """
    logging.info(f"查询合著关系: {rel_query}")
    rel_data = neo4j_conn.run_query(rel_query)

    neo4j_conn.close()

    # 节点列表，边列表
    nodes = []
    edges = []

    for node in node_data:
        # 根据节点的度分配节点大小
        weight = round(node['weight'], 2) if node['weight'] is not None else 0.00
        width_height = weight * 20 + 50

        # 节点格式
        school_node = {
            'data': {
                'id': str(node['id']),
                'name': node['name'],
                'label': '高校人员',
                'unit': node['unit'],
                'section': node['section'],
                'post': str(node['post']),
                'weight': str(weight),
                'coreValue': str(node['coreValue']),
                'communityId': str(node['communityId']),
            },
            'style': {
                'width': width_height,
                'height': width_height,
                'background-color': '#6CB6FF'
            }
        }
        nodes.append(school_node)

    logging.info("高校节点生成")

    for rel in rel_data:
        # 一度关系 边格式
        patent_rel = {
            'data': {
                'source': str(rel['source']),
                'target': str(rel['target']),
                'label': str(rel['type']),
            }
        }
        edges.append(patent_rel)

    logging.info("高校合著关系生成")

    # 图：节点+边
    elements = nodes + edges
    return elements


# ========================== 专利合著网络图 ============================
# 启用额外的布局算法
patent_network = html.Div([
    cyto.Cytoscape(
        id='patent-network',
        elements=school_patent_network("清华大学", "计算机科学与技术系"),
        layout={
            'name': 'cose',
            'idealEdgeLength': 100,
            'nodeOverlap': 20,
            'refresh': 20,
            'randomize': False,
            'componentSpacing': 100,
            'nodeRepulsion': 400000,
            'edgeElasticity': 100,
            'nestingFactor': 5,
            'gravity': 80,
            'numIter': 1000,
            'initialTemp': 200,
            'coolingFactor': 0.95,
            'minTemp': 1.0,
            'fit': True  # 添加 fit 参数
        },
        # style={'width': '100%', 'height': '100%'},
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
                    # 'label': 'data(label)',
                }
            }
        ]
    )], style={
            'height': 'calc(100vh - 40px)',  # 高度占满视口高度减去顶部导航栏的高度
            'width': '100%',
            # 'border': '2px solid #ccc',
            # 'borderRadius': '10px',
            'backgroundColor': '#f0f0f0'
        }
    )


@dash.callback(
    Output("patent-network", "elements"),
    [Input("school-select", "value"),
     Input("college-select", "value")],
    prevent_initial_call=True  # 防止初始时执行
)
def update_social_graph(school, college):
    if school and college:
        elements = school_patent_network(school, college)
        return elements

    # 默认返回空列表
    return school_patent_network("清华大学", "计算机科学与技术系")


# ============================= 页面布局 ===============================
layout = dbc.Container([
    dbc.Row([
        # 筛选框：学校-学院
        dbc.Col(
            html.Div([
                html.H4("筛选高校", className="text-left fw-bold fs-6", style={"fontFamily": "Arial, sans-serif"}),
                school_filter,
                html.Br(),
                html.H4("筛选学院", className="text-left fw-bold fs-6", style={"fontFamily": "Arial, sans-serif"}),
                college_filter
            ],
                style={
                    'backgroundColor': '#f8f9fa',
                    # 'padding': '20px',
                    'borderRadius': '10px',
                    'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
                }
            ),
            width=2
        ),
        # 主内容区
        dbc.Col(
            html.Div([
                patent_network
            ]),
            width=8
        )
    ])
], fluid=True)


layout2 = html.Div(
    [
        # 左侧栏
        html.Div(
            [
                html.H3(
                    "筛选栏",
                    className="text-center fw-bold",
                    style={
                        "textAlign": "center",
                    }
                ),
                html.H4("筛选高校", className="text-left fw-bold fs-6", style={"fontFamily": "Arial, sans-serif"}),
                school_filter,
                html.Br(),
                html.H4("筛选学院", className="text-left fw-bold fs-6", style={"fontFamily": "Arial, sans-serif"}),
                college_filter
            ],
            style={
                "flex": "1",
                "padding": "20px",
                "borderRight": "1px solid #ddd",
                "height": "100vh",
                "overflowY": "auto",
            },
        ),
        # 中间栏
        html.Div(
            [
                patent_network
            ],
            style={
                "flex": "3",
                "padding": "20px",
                "borderRight": "1px solid #ddd",
                "height": "100vh",
                "overflowY": "auto",
                "backgroundColor": "#f8f9fa",
            },
        ),
        # 右侧栏
        html.Div(
            [
                html.H3("右侧栏", style={"textAlign": "center"}),
                html.P("这里是右侧栏的内容", style={"textAlign": "center"}),
            ],
            style={
                "flex": "1",
                "padding": "20px",
                "height": "100vh",
                "overflowY": "auto",
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
        "height": "100vh",
    },
)



if __name__ == '__main__':
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            # 'https://cdn.bootcdn.net/ajax/libs/twitter-bootstrap/5.3.3/css/bootstrap.min.css',   # 国内镜像源
            # 'https://at.alicdn.com/t/font_367131_xd3dpkl99n.css',  # 阿里巴巴矢量图标库
            dbc.themes.LUMEN
        ],
        suppress_callback_exceptions=True
    )
    app.layout = layout2
    app.run(debug=True)
