import dash
from dash import dcc, Output
from dash_extensions.enrich import html, callback, State, Trigger
import dash_bootstrap_components as dbc

from services import application

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        dcc.Location(id="home_url", refresh=True),
        html.H1("Login/Register"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Username"),
                dbc.Input(placeholder="Enter name..", id="user_input"),
                dbc.Button("Login", id="login_user"),
            ]
        ),
    ]
)


@callback(
    Output("home_url", "pathname"),
    Trigger("login_user", "n_clicks"),
    State("user_input", "value"),
)
def login(name):
    application.login(name)
    return "/course-breakdown"
