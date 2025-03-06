import dash
from dash import html
import dash_bootstrap_components as dbc
from dash_extensions.enrich import callback, Trigger, Output, State

import services

dash.register_page(__name__)

layout = dbc.Row(
    [
        html.H2("Course Breakdown"),

        dbc.InputGroup([
            dbc.InputGroupText("New Module"),
            dbc.Input(placeholder="Enter name..", id='new_module_name'),
            dbc.Button("+", id="add_module")
        ]),
        dbc.Row(id="modules")
    ]
)


@callback(
    Output("new_module_name", "invalid"),
    Trigger("add_module", "n_clicks"),
    State("new_module_name", "value")
)
def add_module(new_module_name: str) -> None:
    user = services.application.get_user()
    if new_module_name not in user.modules:
        user.modules.append(new_module_name)
        services.application.update_user(user)
    return new_module_name in user.modules
