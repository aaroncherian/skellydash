from dash import Dash, dcc, html, Output, Input, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

from data_utils import load_and_process_data
from plotting_utils import subsample_and_create_figure
from ui_components import create_gauges_UI, display_marker_list
from layout_components import get_layout
from callback_utils import get_selected_marker, update_marker_buttons, create_trajectory_plots

from pathlib import Path
# Load and process data
try:

    path_to_freemocap_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz_transformed.npy")
    path_to_qualisys_array = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy"

    dataframe_of_3d_data = load_and_process_data(path_to_freemocap_array, path_to_qualisys_array)
except Exception as e:
    print(f"An error occurred: {e}")
    raise

app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')
color_of_cards = '#F3F5F7'


# Create marker figure with subsampled data
marker_figure = subsample_and_create_figure(dataframe_of_3d_data)
marker_figure.update_layout(paper_bgcolor=color_of_cards, plot_bgcolor=color_of_cards)

rmse_values = {
    'total': 20,
    'x': 10,
    'y': 5,
    'z': 5
}
gauges = create_gauges_UI(rmse_values)
# Create gauge figures

# Set the layout
app.layout = get_layout(marker_figure, gauges, color_of_cards)


@app.callback(
    [Output('selected-marker', 'children'),
     Output({'type': 'marker-button', 'index': ALL}, 'className'),
     Output('trajectory-plots', 'children')],
    [Input('main-graph', 'clickData'),
     Input('main-graph', 'hoverData'),
     Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],
    [State('selected-marker', 'children'),
     State({'type': 'marker-button', 'index': ALL}, 'id')]
)

@app.callback(
    [Output('selected-marker', 'children'),
     Output({'type': 'marker-button', 'index': ALL}, 'className'),
     Output('trajectory-plots', 'children')],
    [Input('main-graph', 'clickData'),
     Input('main-graph', 'hoverData'),
     Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],
    [State('selected-marker', 'children'),
     State({'type': 'marker-button', 'index': ALL}, 'id')]
)
def display_trajectories(clickData, hoverData, marker_clicks, selected_marker, button_ids):
    marker = get_selected_marker(clickData, hoverData, selected_marker)
    updated_classnames = update_marker_buttons(marker, button_ids, hoverData)
    trajectory_plots = create_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards)
    
    return marker, updated_classnames, trajectory_plots


if __name__ == '__main__':
    app.run_server(debug=False)