import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, register_page, no_update, Input, ALL
from dash.development.base_component import Component
from dash_extensions.enrich import callback, ctx, Trigger, Output, State, MATCH

import services
from data import Module
from logic import score_needed

register_page(__name__)


def module_input(i, module_data: (str, Module), disabled: bool = False):
    name, module = module_data
    return dbc.InputGroup(
        [
            dbc.Col(
                dbc.Input(
                    value=name,
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
            dbc.Col(
                dbc.Button(
                    "Save",
                    id={"type": "update_module_name", "index": i},
                    disabled=disabled,
                ),
                width=2,
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
                        dbc.Col(
                            dbc.Button(
                                "Save",
                                id="total_update",
                            ),
                            width=2,
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
    user = services.logic.get_user()
    if new_module_name not in user.get_module_names():
        user.add_module(new_module_name)
        services.logic.update_user(user)
        return False, ""
    return True, no_update


@callback(
    Output("modules", "children"),
    Output("course_url", "pathname"),
    Trigger("add_module", "n_clicks"),
    Trigger("course_url", "pathname"),
)
def update_modules() -> Component:
    user = services.logic.get_user()
    if not user:
        return [], "/"
    return (
        [
            module_input(i, module)
            for i, module in enumerate(services.logic.get_user().get_modules().items())
        ],
        no_update,
    )


@callback(
    Output("total_credits", "value"),
    Output("total_score", "value"),
    Trigger("total_update", "n_clicks"),
    State({"type": "modules", "index": ALL}, "value"),
    Input({"type": "module_credits", "index": ALL}, "value"),
    Input({"type": "module_scores", "index": ALL}, "value"),
)
def update_all(module_names, module_credits, module_scores):
    user = services.logic.get_user()
    modules = user.get_module_names()
    for i, (module_name, module_credit, score) in enumerate(
        zip(module_names, module_credits, module_scores)
    ):
        module = modules[i]
        new_module = user.modules[module]  # TODO: refactor updating module
        new_module.credits = module_credit
        new_module.score = score
        user.update_module_name(module, module_name)
        user.update_module_details(module_name, new_module)
    services.logic.update_user(user)
    return (
        sum(module_credits),
        sum(
            module_credit * module_score / 100
            for module_credit, module_score in zip(module_credits, module_scores)
            if module_score is not None
        ),
    )


@callback(
    Output({"type": "update_module_name", "index": MATCH}, "n_clicks"),
    Trigger({"type": "update_module_name", "index": MATCH}, "n_clicks"),
    State({"type": "modules", "index": MATCH}, "value"),
    State({"type": "module_credits", "index": MATCH}, "value"),
    State({"type": "module_scores", "index": MATCH}, "value"),
)
def update_module(module_name, module_credit, score):
    user = services.logic.get_user()
    module = user.get_module_names()[ctx.triggered_id["index"]]
    new_module = user.modules[module]
    new_module.credits = module_credit
    new_module.score = score
    user.update_module_name(module, module_name)
    user.update_module_details(module_name, new_module)
    services.logic.update_user(user)
    return dash.no_update


@callback(
    Output("distinction_score", "value"),
    Output("merit_score", "value"),
    Output("pass_score", "value"),
    Input("total_credits", "value"),
    Input("total_score", "value"),
    Input({"type": "module_scores", "index": ALL}, "value"),
    Input({"type": "module_credits", "index": ALL}, "value"),
)
def update_needed_scores(total_credits, total_score, module_scores, module_credits):
    credits_so_far = sum(
        module_credit
        for module_credit, module_score in zip(module_credits, module_scores)
        if module_score is not None
    )
    return [
        f"{score_needed(total_credits, total_score, credits_so_far, target_score):.1f}"
        for target_score in [0.7, 0.6, 0.5]
    ]
