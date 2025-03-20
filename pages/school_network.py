import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from components import Navbar, DropdownMenu, Accordion  # , Tabs, Cytoscapes, Buttons, Modals
from callbacks import school_filter_callbacks  # , store_callbacks, school_graph_callbacks, school_form_callbacks


dash.register_page(__name__, path="/school_network")  # 使用 `dash.pages`


layout = html.Div([
    dbc.Row([
        dcc.Store(id="selected_school_college"),
        # 左侧边栏：高校-学院列表
        dbc.Col(
            Accordion.school_accordion(),  # 筛选器
            width=2,
            style={
                'backgroundColor': '#f8f9fa',
                # 'padding': '20px',
                'borderRadius': '10px',
                # 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
            }
        ),
        # # 主内容区
        # dbc.Col(
        #     html.Div([
        #         dbc.Card([
        #             dbc.CardHeader(Tabs.network_tabs()),  # 标签页：现有网络/预期网络
        #             dbc.CardBody(
        #                 Cytoscapes.social_graph()  # 社交网络图
        #             ),
        #         ], style={
        #             'width': '100%'
        #             }
        #         ),
        #     ]),
        #     width=8,
        #     # style={'padding': '20px'}
        # ),
        # # 右侧边栏：节点增删改查
        # dbc.Col(
        #     Buttons.add_contacts_button(),  # 添加联系人按钮
        #     width=2,
        #     style={
        #         'backgroundColor': '#f8f9fa',
        #         # 'padding': '20px',
        #         # 'borderRadius': '10px',
        #         # 'boxShadow': '0px 4px 6px rgba(0, 0, 0, 0.1)'
        #     }
        # ),
        # # 弹窗
        # Modals.school_contacts_modal()  # 添加联系人表单弹窗
    ]),
])


# 更新高校筛选
school_filter_callbacks.school_filter_callbacks()
# # 更新高校关系图
# store_callbacks.selected_store_callbacks()
# school_graph_callbacks.update_graph_callback()
# # 添加节点
# school_form_callbacks.add_school_contact_callback()
# school_form_callbacks.update_school_college_callback()
