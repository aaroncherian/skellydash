import dash
from dash import Dash, Output, Input, State, ALL

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

from data_utils.load_data import combine_freemocap_and_qualisys_into_dataframe
from data_utils.file_manager import FileManager

from ui_components.dashboard import prepare_dashboard_elements, update_joint_plots, update_joint_marker_card


from layout.main_layout import get_layout
from callback_utils import get_selected_marker, update_marker_buttons

import numpy as np

COLOR_OF_CARDS = '#F3F5F7'
FRAME_SKIP_INTERVAL = 50

def generate_dash_app(dataframe_of_3d_data, rmse_error_dataframe, absolute_error_dataframe):
    # Initialize Dash App
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    load_figure_template('LUX')

    # Create Figures and Components
    scatter_3d_figure, indicators, marker_buttons_list, joint_rmse_plot= prepare_dashboard_elements(dataframe_of_3d_data, rmse_error_dataframe, FRAME_SKIP_INTERVAL, COLOR_OF_CARDS)

    app.layout = get_layout(marker_figure=scatter_3d_figure, joint_rmse_figure=joint_rmse_plot, list_of_marker_buttons=marker_buttons_list, indicators=indicators, color_of_cards=COLOR_OF_CARDS)


    # Define a Dash callback that listens to multiple inputs and updates multiple outputs
    @app.callback(
        [Output('selected-marker', 'children'),  # Output 1: Change the text displaying the selected marker
        Output('selected-marker-absolute-error', 'children'),
        Output('selected-marker-shading-error', 'children'),
        Output('info-marker-name', 'children'),
        Output('info-x-rmse', 'children'),
        Output('info-y-rmse', 'children'),
        Output('info-z-rmse', 'children'),
        Output({'type': 'marker-button', 'index': ALL}, 'className'),  # Output 2: Update the class names of all marker buttons
        Output('trajectory-plots', 'children'),  # Output 3: Update the trajectory plots
        Output('error-plots', 'children'),  # Output 4: Update the error plots
        Output('error-shading-plots', 'children')],  # Output 5: Update the error shading plots
        [Input('main-graph', 'clickData'),  # Input 1: Listen for clicks on the main graph
        Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],  # Input 3: Listen for clicks on any marker button
        [State('selected-marker', 'children'),  # State 1: The currently selected marker
        State({'type': 'marker-button', 'index': ALL}, 'id')]  # State 2: The IDs of all marker buttons
    )

    def display_trajectories(clickData, marker_clicks, selected_marker, button_ids):
        print("Callback triggered")
        ctx = dash.callback_context
        print(f"Context triggered by: {ctx.triggered}")
        
        if not ctx.triggered:
            print("No trigger found")
            return dash.no_update
        
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(f"Input ID: {input_id}")

        marker = get_selected_marker(input_id, clickData, selected_marker)
        print(f"Selected marker: {marker}")
        # Update the class names of the marker buttons based on the selected marker
        updated_classnames = update_marker_buttons(marker, button_ids)

        # Create and update joint/marker plots based on the selected marker
        trajectory_plots,absolute_error_plots, shaded_error_plots =  update_joint_plots(marker, dataframe_of_3d_data, absolute_error_dataframe, COLOR_OF_CARDS)
        
        x_rmse, y_rmse, z_rmse = update_joint_marker_card(marker, rmse_error_dataframe)

        # Return the updated information for the outputs
        return marker, marker, marker, marker, x_rmse, y_rmse, z_rmse, updated_classnames, trajectory_plots, absolute_error_plots,shaded_error_plots

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
        