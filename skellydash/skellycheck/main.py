import dash
from dash import Dash, Output, Input, State, ALL, dcc

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from data_utils.load_data import combine_freemocap_and_qualisys_into_dataframe
from data_utils.file_manager import FileManager

from ui_components.dashboard import prepare_dashboard_elements, update_joint_plots, update_joint_marker_card

from layout.main_layout import get_layout

from callback_utils import get_selected_marker, update_marker_buttons
from callbacks.marker_name_callbacks import register_marker_name_callbacks
from callbacks.selected_marker_callback import register_selected_marker_callback

import numpy as np

COLOR_OF_CARDS = '#F3F5F7'
FRAME_SKIP_INTERVAL = 50


def generate_dash_app(dataframe_of_3d_data, rmse_error_dataframe, absolute_error_dataframe):
    # Initialize Dash App
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    register_selected_marker_callback(app) #register a callback to find the selected marker and stored it
    register_marker_name_callbacks(app) #register a callback to update the marker name wherever it is listed in the app

    load_figure_template('LUX')

    # Create Figures and Components
    scatter_3d_figure, indicators, marker_buttons_list, joint_rmse_plot = prepare_dashboard_elements(
        dataframe_of_3d_data, rmse_error_dataframe, FRAME_SKIP_INTERVAL, COLOR_OF_CARDS)

    app.layout = get_layout(marker_figure=scatter_3d_figure,
                            joint_rmse_figure=joint_rmse_plot,
                            list_of_marker_buttons=marker_buttons_list,
                            indicators=indicators,
                            color_of_cards=COLOR_OF_CARDS)


    # Define a Dash callback that listens to multiple inputs and updates multiple outputs
    @app.callback(
        [Output('info-x-rmse', 'children'),
        Output('info-y-rmse', 'children'),
        Output('info-z-rmse', 'children'),
        Output({'type': 'marker-button', 'index': ALL}, 'className'),
        Output('trajectory-plots', 'children'),
        Output('error-plots', 'children'),
        Output('error-shading-plots', 'children')],
        [Input('store-selected-marker', 'data')],
        [State({'type': 'marker-button', 'index': ALL}, 'id')]
    )
    def display_trajectories(stored_data, button_ids):
        marker = stored_data['marker'] if stored_data else None

        # Update the class names of the marker buttons based on the selected marker
        updated_classnames = update_marker_buttons(marker, button_ids)
        
        # Create and update joint/marker plots based on the selected marker
        trajectory_plots, absolute_error_plots, shaded_error_plots = update_joint_plots(
            marker, dataframe_of_3d_data, absolute_error_dataframe, COLOR_OF_CARDS
        )
        
        x_rmse, y_rmse, z_rmse = update_joint_marker_card(marker, rmse_error_dataframe)

        # Return the updated information for the outputs
        return x_rmse, y_rmse, z_rmse, updated_classnames, trajectory_plots, absolute_error_plots, shaded_error_plots
        
    app.run_server(debug=False)


if __name__ == '__main__':

        
    from pathlib import Path

    path_to_recording_folder = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3")

    file_manager = FileManager(path_to_recording_folder)
    freemocap_data = file_manager.freemocap_data
    qualisys_data = file_manager.qualisys_data
    rmse_error_dataframe = file_manager.rmse_error_dataframe
    absolute_error_dataframe = file_manager.absolute_error_dataframe
    dataframe_of_3d_data = combine_freemocap_and_qualisys_into_dataframe(freemocap_3d_data=freemocap_data, qualisys_3d_data=qualisys_data)

    generate_dash_app(dataframe_of_3d_data, rmse_error_dataframe, absolute_error_dataframe)
        