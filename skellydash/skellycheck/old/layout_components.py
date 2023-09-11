from dash import dcc, html
import dash_bootstrap_components as dbc


def create_card(title, content, color_of_cards):
    return dbc.Card([
        dbc.CardHeader(
            html.H2(title, className="text-primary"),
            className="text-primary"
        ),
        dbc.CardBody(content, style={"backgroundColor": color_of_cards}),
    ], className="mb-4 mt-4")

def get_scatter_plot_card(marker_figure, color_of_cards):
    content = [dcc.Graph(id='main-graph', figure=marker_figure)]
    return create_card("3D Scatter Plot", content, color_of_cards)

def get_marker_list_card(marker_list, color_of_cards):
    content = [
        dbc.Row([
            dbc.Col([
                html.Div(
                    id='marker-list',
                    children=marker_list,
                    style={'display': 'flex', 'flexWrap': 'wrap'}
                )
            ])
        ])
    ]
    return create_card("Marker List", content, color_of_cards)

def get_marker_trajectory_card(color_of_cards):
    content = [
        html.H3(
            id='selected-marker',
            children="Select a marker",
            className="text-info"
        ),
        html.Div(id='trajectory-plots')
    ]
    return create_card("Marker Trajectory", content, color_of_cards)

def get_rmse_card(gauges):
    content = [
        html.Div(
            id='rmse-gauges',
            children=gauges,
            style={'display': 'flex'}
        )
    ]
    return create_card("RMSE", content, None)

def get_layout(marker_figure, marker_list, gauges, color_of_cards):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                get_scatter_plot_card(marker_figure, color_of_cards),
                get_marker_list_card(marker_list, color_of_cards),
            ], md=6, style={'height': '100vh'}),
            dbc.Col(
                get_marker_trajectory_card(color_of_cards),
                md=5
            )
        ]),
        dbc.Row(
            get_rmse_card(gauges)
        )
    ], fluid=True)