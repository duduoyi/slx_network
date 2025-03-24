import dash
from dash import html, Input, Output, State
from flask_login import current_user
from components import Navbar, DropdownMenu, Buttons
import logging


def navbar_callbacks():
    @dash.callback(
        Output('navbar-menu', 'children'),
        Output('navbar-user', 'children'),
        Input('url', 'pathname'),
    )
    def navbar_change(pathname):
        if current_user.is_authenticated:
            logging.info(f'用户已登录 {current_user.is_authenticated}')
            return html.Div([Navbar.menu()]), html.Div([DropdownMenu.user_features()])
        logging.info(f'用户未登录')
        return html.Div(), html.Div([Buttons.home_login_button()])