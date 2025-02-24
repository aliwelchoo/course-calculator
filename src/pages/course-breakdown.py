import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Row(
    [
        html.H2("Course Breakdown"),

        dbc.InputGroup([
            dbc.InputGroupText("New Module"),
            dbc.Input(placeholder="Enter name..", id='new_module_name'),
            dbc.Button("+", id="add_module")
        ])
    ]
)
