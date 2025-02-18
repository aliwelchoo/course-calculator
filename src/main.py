import dash
from dash import Dash, html, dcc

import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True)

app.layout = dbc.Container(dbc.Row(
    [
        html.H1("Course Calculator"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}", href=page["relative_path"]
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dbc.Row(dash.page_container),
    ]),
    fluid=True
)

if __name__ == "__main__":
    app.run(debug=True)
