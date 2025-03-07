import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, register_page, no_update, Input, set_props
from dash.development.base_component import Component
from dash_extensions.enrich import callback, ctx, Trigger, Output, State, MATCH

import services
from logic import Module

register_page(__name__)


def module_input(i, module: Module):
    return dbc.InputGroup(
        [
            dbc.Col(
                dbc.Input(
                    value=module.name,
                    id={"type": "modules", "index": i},
                ),
                width=4,
            ),
            dbc.Col(dbc.InputGroupText("Credits"), width=2),
            dbc.Col(
                dbc.Input(
                    value=module.credits,
                    id={"type": "module_credits", "index": i},
                    type="number",
                ),
                width=1,
            ),
            dbc.Col(dbc.InputGroupText("Score"), width=2),
            dbc.Col(
                dbc.Input(
                    value=module.score,
                    id={"type": "module_scores", "index": i},
                    type="number",
                ),
                width=1,
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
        html.Br(),
        dbc.Row(id="modules"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.InputGroup(
                    [
                        dbc.Col(
                            dbc.Input(
                                value="Total",
                                disabled=True,
                            ),
                            width=4,
                        ),
                        dbc.Col(dbc.InputGroupText("Total Credits"), width=2),
                        dbc.Col(
                            dbc.Input(
                                id="total_credits",
                                type="number",
                                disabled=True,
                            ),
                            width=1,
                        ),
                        dbc.Col(dbc.InputGroupText("Total Score"), width=2),
                        dbc.Col(
                            dbc.Input(
                                id="total_score",
                                type="number",
                                disabled=True,
                            ),
                            width=1,
                        ),
                    ]
                ),
            ]
        ),
        html.Br(),
        html.Br(),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Score needed for Pass"),
                dbc.Col(
                    dbc.Input(
                        id="pass_score",
                        type="number",
                        disabled=True,
                    ),
                    width=1,
                ),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Score needed for Merit"),
                dbc.Col(
                    dbc.Input(
                        id="merit_score",
                        type="number",
                        disabled=True,
                    ),
                    width=1,
                ),
            ]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText("Score needed for Distinction"),
                dbc.Col(
                    dbc.Input(
                        id="distinction_score",
                        type="number",
                        disabled=True,
                    ),
                    width=1,
                ),
            ]
        ),
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
    if new_module_name not in user.get_module_names():
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
    set_props("total_credits", {"value": user.total_credits})
    set_props("total_score", {"value": user.score_so_far})
    return (
        [module_input(i, module) for i, module in enumerate(user.get_modules())],
        no_update,
    )


@callback(
    Output({"type": "modules", "index": MATCH}, "value"),
    Input({"type": "modules", "index": MATCH}, "value"),
    Input({"type": "module_credits", "index": MATCH}, "value"),
    Input({"type": "module_scores", "index": MATCH}, "value"),
)
def update_module(module_name, module_credit, score):
    user = services.application.get_user()
    module = user.get_module_names()[ctx.triggered_id["index"]]
    user.update_module_name(module, module_name)
    user.update_module(module_name, Module(module_name, module_credit, score))
    services.application.update_user(user)
    set_props("total_credits", {"value": user.total_credits})
    set_props("total_score", {"value": user.score_so_far})
    return dash.no_update


@callback(
    Output("distinction_score", "value"),
    Output("merit_score", "value"),
    Output("pass_score", "value"),
    Trigger("total_credits", "value"),
    Trigger("total_score", "value"),
)
def update_needed_scores():
    user = services.application.get_user()
    return [
        f"{user.score_needed(target_score):.1f}" for target_score in [0.7, 0.6, 0.5]
    ]
