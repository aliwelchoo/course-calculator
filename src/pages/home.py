import dash
from dash_extensions.enrich import html, callback, State, Trigger
import dash_bootstrap_components as dbc

from src.services import application

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.H1("Login/Register"),
        dbc.InputGroup([
            dbc.InputGroupText("Username"),
            dbc.Input(placeholder="Enter name..", id='user_input'),
            dbc.Button("Login", id="login_user")
        ])
    ]
)


@callback(
    Trigger("login_user", "n_clicks"),
    State("user_input", "children")
)
def login(name):
    application.login(name)
