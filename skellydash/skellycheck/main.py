from dash import Dash, Output, Input, State, ALL
import dash
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

from data_utils.load_data import combine_freemocap_and_qualisys_into_dataframe
from data_utils.sample_data import subsample_dataframe
from plotting_utils import create_3d_scatter_from_dataframe, create_trajectory_plots, create_rmse_bar_plot, create_error_plots, create_error_shading_plots
from ui_components import create_gauges_UI, display_marker_list
from layout.main_layout import get_layout
from callback_utils import get_selected_marker, update_marker_buttons

from pathlib import Path
import pandas as pd
import numpy as np
# Load and process data

class FileManager:
    def __init__(self, path_to_recording_folder: Path):
        self.path_to_recording_folder = path_to_recording_folder
        self.run()

    def run(self):
        self._build_paths()
        self._load_data()

    def _build_paths(self):
        path_to_output_data_folder = self.path_to_recording_folder/'output_data'
        self.path_to_freemocap_array = path_to_output_data_folder/'mediapipe_body_3d_xyz_transformed.npy'
        self.path_to_qualisys_array = self.path_to_recording_folder/'qualisys'/'clipped_qualisys_skel_3d.npy'
        self.rmse_csv_path = path_to_output_data_folder/'rmse_dataframe.csv'
        self.absolute_error_csv_path = path_to_output_data_folder/'absolute_error_dataframe.csv'

    def _load_data(self):
        self.freemocap_data = self._load_if_exists(self.path_to_freemocap_array)
        self.qualisys_data = self._load_if_exists(self.path_to_qualisys_array)
        self.rmse_error_dataframe = self._load_csv_if_exists(self.rmse_csv_path)
        self.absolute_error_dataframe = self._load_csv_if_exists(self.absolute_error_csv_path)

    def _load_if_exists(self, path: Path):
        if path.exists():
            return np.load(path)
        else:
            print(f"Warning: File {path} does not exist.")
            return None

    def _load_csv_if_exists(self, path: Path):
        if path.exists():
            return pd.read_csv(path)
        else:
            print(f"Warning: File {path} does not exist.")
            return None




def generate_dash_app(dataframe_of_3d_data, rmse_error_daframe, absolute_error_dataframe):
    app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    load_figure_template('LUX')
    color_of_cards = '#F3F5F7'


    # Create marker figure with subsampled data
    subsampled_dataframe = subsample_dataframe(dataframe=dataframe_of_3d_data, frame_skip_interval=50)
    marker_figure = create_3d_scatter_from_dataframe(dataframe_of_3d_data=subsampled_dataframe)
    marker_figure.update_layout(paper_bgcolor=color_of_cards, plot_bgcolor=color_of_cards)

    total_rmse = rmse_error_daframe.loc[(rmse_error_daframe['marker'] == 'All') & (rmse_error_daframe['coordinate'] == 'All'), 'RMSE'].values[0]
    x_rmse = rmse_error_daframe.loc[(rmse_error_daframe['marker'] == 'All') & (rmse_error_daframe['coordinate'] == 'x_error'), 'RMSE'].values[0]
    y_rmse = rmse_error_daframe.loc[(rmse_error_daframe['marker'] == 'All') & (rmse_error_daframe['coordinate'] == 'y_error'), 'RMSE'].values[0]
    z_rmse = rmse_error_daframe.loc[(rmse_error_daframe['marker'] == 'All') & (rmse_error_daframe['coordinate'] == 'z_error'), 'RMSE'].values[0]


    rmse_values = {
        'total': total_rmse,
        'x': x_rmse,
        'y': y_rmse,
        'z': z_rmse
    }
    gauges = create_gauges_UI(rmse_values)
    # Create gauge figures
    marker_list = display_marker_list(dataframe_of_3d_data)
    # Set the layout

    joint_rmse_plot = create_rmse_bar_plot(rmse_error_daframe)

    app.layout = get_layout(marker_figure=marker_figure, joint_rmse_figure=joint_rmse_plot, list_of_marker_buttons=marker_list, gauges=gauges, color_of_cards=color_of_cards)


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
        # Create and update the trajectory plots based on the selected markerAgain, 
        trajectory_plots = create_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards)

        error_plots = create_error_plots(marker, absolute_error_dataframe, color_of_cards)

        trajectory_with_error_plots = create_error_shading_plots(marker, dataframe_of_3d_data, absolute_error_dataframe, color_of_cards)
        
        rmses_for_this_marker = rmse_error_daframe[rmse_error_daframe.marker == marker][['coordinate','RMSE']]

        selected_data_indexed = rmses_for_this_marker.set_index('coordinate')
        x_error_rmse = np.round(selected_data_indexed.at['x_error', 'RMSE'],2)
        y_error_rmse = np.round(selected_data_indexed.at['y_error', 'RMSE'],2)
        z_error_rmse = np.round(selected_data_indexed.at['z_error', 'RMSE'],2)

        # Return the updated information for the outputs
        return marker, marker, marker, marker, x_error_rmse, y_error_rmse, z_error_rmse, updated_classnames, trajectory_plots, error_plots,trajectory_with_error_plots

    app.run_server(debug=False)
if __name__ == '__main__':

    path_to_recording_folder = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3")

    file_manager = FileManager(path_to_recording_folder)
    freemocap_data = file_manager.freemocap_data
    qualisys_data = file_manager.qualisys_data
    rmse_error_daframe = file_manager.rmse_error_dataframe
    absolute_error_dataframe = file_manager.absolute_error_dataframe
    dataframe_of_3d_data = combine_freemocap_and_qualisys_into_dataframe(freemocap_3d_data=freemocap_data, qualisys_3d_data=qualisys_data)

    generate_dash_app(dataframe_of_3d_data, rmse_error_daframe, absolute_error_dataframe)
        