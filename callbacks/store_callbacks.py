import json
import dash
from dash import Input, Output, State, callback_context, ALL
from dash.exceptions import PreventUpdate
from utils import filter_list_of_user


def selected_store_callbacks():
    @dash.callback(
        Output("selected_school_college", "data"),
        Input({'type': 'list-item', 'index': ALL}, 'n_clicks'),
        [State("login-user", "data"),
         State("selected_school_college", "data")],  # 之前的选择
    )
    def store_selected_college(n_clicks, store_user, current_selection):
        """ 处理默认选择和点击选择 """
        if not store_user:
            raise PreventUpdate  # 如果没有用户数据，不执行回调
        # 获取用户登录信息
        login_name = store_user.get("username")
        login_unit = store_user.get("unit")
        login_section = store_user.get("section")
        login_type = store_user.get("user_type")
        # 获取默认的学校-学院
        school_college = filter_list_of_user.school_contact_list(login_type, login_unit, login_section, login_name)
        default_school = school_college['school'][0]
        default_college = school_college['college'][0]
        default_index = f"{default_school}_{default_college}"
        print(f"默认选择: {default_index}")
        # 判断回调触发来源
        if callback_context.triggered:
            triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
            print("Triggered ID:", triggered_id)
            try:
                triggered_dict = json.loads(triggered_id)  # 获取点击的学院信息
                selected_index = triggered_dict.get("index")
                print("Selected Index:", selected_index)
                return selected_index
            except json.JSONDecodeError:
                pass  # 处理异常情况，保持现有数据
        # 返回默认选项（页面初次加载或无有效点击时）
        return default_index if current_selection is None else current_selection
