import json
import dash
from dash import Input, Output, State, callback_context, ALL
from utils import social_graph_of_school_now, social_graph_of_school_expect


def update_graph_callback():
    @dash.callback(
        Output("social_graph", "elements"),
        [Input("tabs", "active_tab"),
         Input({'type': 'list-item', 'index': ALL}, 'n_clicks')],
        [State("login-user", "data"),
         State("selected_school_college", "data")],
        prevent_initial_call=True  # 防止初始时执行
    )
    def update_social_graph(selected_graph, n_clicks, store_user_data, stored_college):
        if store_user_data is None:
            return []

        # 提取登录用户信息
        login_name = store_user_data.get("username")
        login_unit = store_user_data.get("unit")
        login_section = store_user_data.get("section")
        login_type = store_user_data.get("user_type")
        print(stored_college)
        # 提取选择的学校和学院信息
        selected_school, selected_college = stored_college.split('_')

        # 获取社交图的封装函数
        def get_social_graph(graph_type, school, college):
            if graph_type == '现有网络':
                return social_graph_of_school_now.now_social(
                    login_type, login_unit, login_section, login_name,
                    school, college)
            elif graph_type == '预期网络':
                return social_graph_of_school_expect.expect_social(
                    login_type, login_unit, login_section, login_name,
                    school, college)

        # 处理默认的图（如果没有触发事件）
        if not callback_context.triggered:
            return get_social_graph('现有网络', selected_school, selected_college)

        # 获取触发事件的组件ID
        triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]

        # 如果是标签页或列表项触发，统一调用获取社交图的函数
        if 'tabs' in triggered_id or 'list-item' in triggered_id:
            # 如果是列表项触发，解析选中的学院
            if 'list-item' in triggered_id:
                # 提取点击的学院信息
                triggered_dict = json.loads(triggered_id)  # 提取点击的学院信息
                selected_index = triggered_dict.get("index")
                selected_school, selected_college = selected_index.split('_')

            return get_social_graph(selected_graph, selected_school, selected_college)

        # 默认返回空列表
        return []