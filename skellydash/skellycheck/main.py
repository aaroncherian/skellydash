from dash import Dash, Output, Input, State, ALL
import dash
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

from data_utils.load_data import load_and_process_data
from data_utils.sample_data import subsample_dataframe
from plotting_utils import create_3d_scatter_from_dataframe, create_trajectory_plots, create_rmse_bar_plot
from ui_components import create_gauges_UI, display_marker_list
from layout.main_layout import get_layout
from callback_utils import get_selected_marker, update_marker_buttons

from pathlib import Path
import pandas as pd
# Load and process data
try:

    path_to_freemocap_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz_transformed.npy")
    path_to_qualisys_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy")

    dataframe_of_3d_data = load_and_process_data(path_to_freemocap_array, path_to_qualisys_array)

    csv_path = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\rmse_dataframe.csv"
    rmse_error_daframe = pd.read_csv(csv_path)



except Exception as e:
    print(f"An error occurred: {e}")
    raise



app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')
color_of_cards = '#F3F5F7'


# Create marker figure with subsampled data
subsampled_dataframe = subsample_dataframe(dataframe=dataframe_of_3d_data, frame_skip_interval=100)
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

app.layout = get_layout(marker_figure=marker_figure, joint_rmse_figure=joint_rmse_plot, marker_list=marker_list, gauges=gauges, color_of_cards=color_of_cards)


# Define a Dash callback that listens to multiple inputs and updates multiple outputs
@app.callback(
    [Output('selected-marker', 'children'),  # Output 1: Change the text displaying the selected marker
     Output({'type': 'marker-button', 'index': ALL}, 'className'),  # Output 2: Update the class names of all marker buttons
     Output('trajectory-plots', 'children')],  # Output 3: Update the trajectory plots
    [Input('main-graph', 'clickData'),  # Input 1: Listen for clicks on the main graph
     Input('main-graph', 'hoverData'),  # Input 2: Listen for hover events on the main graph
     Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],  # Input 3: Listen for clicks on any marker button
    [State('selected-marker', 'children'),  # State 1: The currently selected marker
     State({'type': 'marker-button', 'index': ALL}, 'id')]  # State 2: The IDs of all marker buttons
)

def display_trajectories(clickData, hoverData, marker_clicks, selected_marker, button_ids):
    # Retrieve information about which input triggered the callback
    ctx = dash.callback_context
    # If the callback was not triggered, do not update anything
    if not ctx.triggered:
        return dash.no_update
    # Extract the input ID that triggered the callback
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Determine the selected marker based on which input triggered the callback
    marker = get_selected_marker(input_id, clickData, selected_marker)
    # Update the class names of the marker buttons based on the selected marker
    updated_classnames = update_marker_buttons(marker, button_ids, hoverData)
    # Create and update the trajectory plots based on the selected marker
    trajectory_plots = create_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards)
    
    # Return the updated information for the outputs
    return marker, updated_classnames, trajectory_plots

if __name__ == '__main__':
    app.run_server(debug=False)