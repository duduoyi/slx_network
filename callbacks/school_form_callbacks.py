import dash
from dash import Input, Output, State, callback_context
from utils import filter_list_of_form, add_contacts_to_neo4j


# 控制 Modal 打开和关闭的回调
def add_school_contact_callback():
    @dash.callback(
        [Output("add-school-modal", "is_open"),
         Output("school-unit-select", "value"),
         Output("school-section-select", "value"),
         Output("school-post-select", "value"),
         Output("school-name-input", "value"),
         Output("school-rel-select", "value")],
        [Input("add-button", "n_clicks"),  # 添加联系人按钮
         Input("submit-school-button", "n_clicks"),   # 提交按钮
         Input("login-user", "data")],
        [State("add-school-modal", "is_open"),
         State("school-unit-select", "value"),
         State("school-section-select", "value"),
         State("school-post-select", "value"),
         State("school-name-input", "value"),
         State("school-rel-select", "value")],
        prevent_initial_call=True  # 防止初始时执行
    )
    def toggle_or_submit_modal(add_button_clicks, submit_button_clicks, data, is_open, unit_value, section_value,
                               post_value, name_input_value, rel_value):
        login_name = data.get("username")
        login_unit = data.get("unit")
        login_section = data.get("section")
        login_type = data.get("user_type")

        # 如果没有点击按钮，保持 Modal 状态不变
        if not callback_context.triggered:
            return is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

        triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0]
        if triggered_id == 'add-button':  # 如果点击了“添加联系人”按钮
            print(f"add_button_clicks: {add_button_clicks}")
            return not is_open, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        elif triggered_id == 'submit-button':  # 如果点击了“提交”按钮
            print(f"submit_button_clicks: {submit_button_clicks}")
            print(f"is_open: {is_open}")
            print(f"unit_value: {unit_value}")
            print(f"section_value: {section_value}")
            print(f"post_value: {post_value}")
            print(f"name_input_value: {name_input_value}")
            print(f"rel_value: {rel_value}")
            # 处理提交逻辑
            add_contacts_to_neo4j.create_node_and_relationship(
                login_type, login_unit, login_section, login_name,
                rel_value, unit_value, section_value, post_value, name_input_value)
            print("已添加联系人")
            # 提交后清空表单
            return False, '', '', '', '', ''  # 关闭 Modal 并清空表单


def update_school_college_callback():
    # 关联筛选
    @dash.callback(
        Output('school-section-select', 'options'),
        Input('school-unit-select', 'value'),
        prevent_initial_call=True  # 防止初始时执行
    )
    def update_college_options(selected_unit):
        if selected_unit:
            # 获取单位列表
            school_data = filter_list_of_form.school_list()
            colleges = school_data[school_data['school'] == selected_unit]['college'].unique()
            return [{'label': college, 'value': college} for college in colleges]
        # 如果没有选择组织，返回空选项
        return []