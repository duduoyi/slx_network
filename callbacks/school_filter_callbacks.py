import dash
from dash import html, Output, Input
import dash_bootstrap_components as dbc
from utils.filter_list_of_user import school_contact_list


def school_filter_callbacks():
    @dash.callback(
        Output('school-accordion', 'children'),
        Input("login-user", "data"),
    )
    def school_filter(store_user):
        print("store_user_data:", store_user)
        login_name = store_user.get("username")
        login_unit = store_user.get("unit")
        login_section = store_user.get("section")
        login_type = store_user.get("user_type")
        # 登陆人关联学校学院
        school_college = school_contact_list(login_type, login_unit, login_section, login_name)
        distinct_school = school_college['school'].unique()

        # 创建学校 Accordion
        accordion_items = []
        for school in distinct_school:
            # 学院列表
            colleges = school_college[school_college['school'] == school]['college'].unique()

            # 创建第二层 Accordion（学院）
            college_items = [
                dbc.ListGroupItem(
                    college,
                    id={"type": "list-item", "index": f"{school}_{college}"},  # 使用字典格式设置 id
                    action=True,
                    n_clicks=0,  # 初始化点击次数为0
                ) for college in colleges
            ]

            # 创建学校的 AccordionItem
            accordion_items.append(
                dbc.AccordionItem(
                    html.Div([
                        dbc.ListGroup(college_items, flush=True)  # 展示学院
                    ]),
                    title=school,  # 学校名称作为标题
                    id=f"{school}_school",  # 学校的唯一 ID
                )
            )
        return accordion_items