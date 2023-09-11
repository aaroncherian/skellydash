import dash_bootstrap_components as dbc
from .cards.marker_trajectory_card import get_marker_trajectory_card
from .cards.marker_buttons_card import get_marker_buttons_card
from .cards.scatter_plot_card import get_scatter_plot_card
from .cards.rmse_card import get_rmse_card
def get_layout(marker_figure, marker_list, gauges, color_of_cards):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                get_scatter_plot_card(marker_figure, color_of_cards),
                get_marker_buttons_card(marker_list, color_of_cards),
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

def get_layout(marker_figure, marker_list, gauges, color_of_cards):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                get_scatter_plot_card(marker_figure, color_of_cards),
                get_marker_buttons_card(marker_list, color_of_cards),
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