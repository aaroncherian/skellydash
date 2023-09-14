import dash_bootstrap_components as dbc
from dash.dcc import Store
from .cards.marker_trajectory_card import get_marker_trajectory_card
from .cards.marker_buttons_card import get_marker_buttons_card
from .cards.scatter_plot_card import get_scatter_plot_card
from .cards.rmse_card import get_rmse_card
from .cards.joint_rmse_plot_card import get_joint_rmse_plot_card
from .cards.absolute_error_plot_card import get_absolute_error_plots_card
from .cards.error_shading_plot_card import get_error_shading_plot_card


def get_layout(marker_figure, joint_rmse_figure, list_of_marker_buttons, gauges, color_of_cards):
    sidebar = dbc.Col(
        [
            get_marker_buttons_card(list_of_marker_buttons, color_of_cards)
        ],
        width={"size": 1, "order": "first"},
        id="sidebar",
    )

    main_content = dbc.Col(
        [
            dbc.Row(
                get_rmse_card(gauges)
            ),
            dbc.Row([
                get_joint_rmse_plot_card(joint_rmse_figure['x_error'], 'X Dimension', color_of_cards),
                get_joint_rmse_plot_card(joint_rmse_figure['y_error'], 'Y Dimension', color_of_cards),
                get_joint_rmse_plot_card(joint_rmse_figure['z_error'], 'Z Dimension', color_of_cards),
            ]),
            dbc.Row([
                dbc.Col(get_scatter_plot_card(marker_figure, color_of_cards), width={"size": 6, "offset": 3})
            ]),
            dbc.Row([
                get_marker_trajectory_card(color_of_cards)
            ]),
            dbc.Row([
                get_absolute_error_plots_card(color_of_cards)
            ]),
            dbc.Row([
                get_error_shading_plot_card(color_of_cards)
            ]),
        ],
        width={"size": 10, "order": "last"},
    )

    return dbc.Container([
        dbc.Row([sidebar, main_content]),
    ], fluid=True)