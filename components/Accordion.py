import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.filter_list_of_user import school_contact_list


def school_accordion():
    return html.Div([
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    [
                        dbc.Accordion(id="school-accordion", start_collapsed=False, flush=True)
                    ],
                    title="高校关系"
                ),
            ],
            flush=True
        )
    ])


# 测试
if __name__ == "__main__":
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = html.Div([
        school_accordion(),  # 筛选器
    ])
    app.run_server(debug=True)


