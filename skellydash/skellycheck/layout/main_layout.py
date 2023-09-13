import dash_bootstrap_components as dbc
from dash.dcc import Store
from .cards.marker_trajectory_card import get_marker_trajectory_card
from .cards.marker_buttons_card import get_marker_buttons_card
from .cards.scatter_plot_card import get_scatter_plot_card
from .cards.rmse_card import get_rmse_card
from .cards.joint_rmse_plot_card import get_joint_rmse_plot_card
from .cards.absolute_error_plot_card import get_absolute_error_plots_card



def get_layout(marker_figure, joint_rmse_figure, marker_list, gauges, color_of_cards):
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
        ),
        dbc.Row([
            get_joint_rmse_plot_card(joint_rmse_figure['x_error'], 'X Dimension', color_of_cards),
            get_joint_rmse_plot_card(joint_rmse_figure['y_error'], 'Y Dimension', color_of_cards),
            get_joint_rmse_plot_card(joint_rmse_figure['z_error'], 'Z Dimension', color_of_cards),
        ]),
        dbc.Row([
            get_absolute_error_plots_card(color_of_cards)
        ])

    ], fluid=True)