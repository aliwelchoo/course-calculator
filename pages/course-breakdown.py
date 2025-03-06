import dash
from dash import html, dcc, register_page, no_update
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
from dash_extensions.enrich import callback, ctx, Trigger, Output, State, MATCH

import services

register_page(__name__)


def module_input(i, name: str, disabled: bool = False):
    return dbc.InputGroup(
        [
            dbc.InputGroupText(i + 1),
            dbc.Input(
                value=name,
                id={"type": "modules", "index": i},
            ),
            dbc.Button(
                "Update name",
                id={"type": "update_module_name", "index": i},
                disabled=disabled,
            ),
        ]
    )


layout = dbc.Row(
    [
        dcc.Location(id="course_url", refresh=True),
        html.H2("Course Breakdown"),
        dbc.InputGroup(
            [
                dbc.InputGroupText("New Module"),
                dbc.Input(placeholder="Enter name..", id="new_module_name"),
                dbc.Button("+", id="add_module"),
            ]
        ),
        dbc.Row(id="modules"),
    ]
)


@callback(
    Output("new_module_name", "invalid"),
    Output("new_module_name", "value"),
    Trigger("add_module", "n_clicks"),
    State("new_module_name", "value"),
)
def add_module(new_module_name: str) -> None:
    user = services.application.get_user()
    if new_module_name not in user.get_modules():
        user.add_module(new_module_name)
        services.application.update_user(user)
        return False, ""
    return True, no_update


@callback(
    Output("modules", "children"),
    Output("course_url", "pathname"),
    Trigger("add_module", "n_clicks"),
    Trigger("course_url", "pathname"),
)
def update_modules() -> Component:
    user = services.application.get_user()
    if not user:
        return [], "/"
    return (
        [
            module_input(i, module)
            for i, module in enumerate(services.application.get_user().get_modules())
        ],
        no_update,
    )


@callback(
    Output({"type": "update_module_name", "index": MATCH}, "n_clicks"),
    Trigger({"type": "update_module_name", "index": MATCH}, "n_clicks"),
    State({"type": "modules", "index": MATCH}, "value")
)
def update_name(new_name):
    user = services.application.get_user()
    module = user.get_modules()[ctx.triggered_id["index"]]
    user.update_module_name(module, new_name)
    services.application.update_user(user)
    return dash.no_update
