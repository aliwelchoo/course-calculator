import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__)

layout = dbc.Row(
    [
        html.H1("Course Breakdown"),

        dbc.InputGroup([
            dbc.InputGroupText("Module name"),
            dbc.Input(placeholder="Enter name.."),
            dbc.Button("+", id="add_module")
        ])

    ]
)
