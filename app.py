import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_extensions.enrich import DashProxy, TriggerTransform

app = DashProxy(
    __name__,
    use_pages=True,
    external_stylesheets=[
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css",
        dbc.themes.FLATLY,
    ],
    transforms=[TriggerTransform()],
    prevent_initial_callbacks=True,
)

app.layout = dbc.Container(
    dbc.Row(
        [
            html.H1("Course Calculator"),
            html.Div(
                [
                    html.Div(
                        dcc.Link(
                            page["name"],
                            href=page["relative_path"],
                            id=page["name"] + "-link",
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            ),
            dbc.Row(dbc.Col(dash.page_container, width={"size": 8, "offset": 2})),
        ]
    ),
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)
