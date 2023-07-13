import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


from full_skeleton_graph import create_skeleton_figure
from pathlib import Path

import plotly.express as px
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

load_figure_template('SOLAR')

# We need to have the figure globally available to access it in the callback
path_to_numpy_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_15_36_03_MDN_OneLeg_Trial1\output_data\mediapipe_body_3d_xyz.npy")

marker_figure, marker_position_df = create_skeleton_figure(path_to_numpy_array)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("3D Scatter Plot", className="text-primary"),
            dcc.Graph(id='main-graph', figure=marker_figure)], 
            md=6, style={'height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}
        ),
        dbc.Col(
            dbc.Container([
                html.H2("Marker Trajectory", className="text-primary"),
                html.H3(id='selected-marker', children="Select a marker", className="text-info"),
                dcc.Graph(id='x-trajectory'),
                dcc.Graph(id='y-trajectory'),
                dcc.Graph(id='z-trajectory'),
            ], style={'height': '100vh', 'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center'}),
            md=6),
    ])
], fluid=True)



@app.callback(
    [Output('x-trajectory', 'figure'),
     Output('y-trajectory', 'figure'),
     Output('z-trajectory', 'figure'),
     Output('selected-marker', 'children')],  # Add this line
    Input('main-graph', 'clickData'),
)

def display_trajectories(clickData):
    # clickData is a dictionary containing information about the point that was clicked
    # see https://dash.plotly.com/interactive-graphing for more info

        # rest of your callback code here
    if clickData is None or 'points' not in clickData or len(clickData['points']) == 0 or 'id' not in clickData['points'][0]:
        return {}, {}, {}, "Select a marker"

    # Assuming the marker name is in clickData, we can find the trajectories
    marker = clickData['points'][0]['id']
    df_marker = marker_position_df[marker_position_df.marker == marker]


    trajectory_plot_height = 350
    fig_x = px.line(df_marker, x='frame', y='x')
    fig_x.update_xaxes(title_text = '', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18, ))

    fig_y = px.line(df_marker, x='frame', y='y')
    fig_y.update_xaxes(title_text = '',showticklabels=False) # Remove X-axis labels for this graph
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18,))
    fig_y.update_layout(margin=dict(t=5), height = trajectory_plot_height) # Adjust top margin


    fig_z = px.line(df_marker, x='frame', y='z')
    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(margin=dict(t=5), height = trajectory_plot_height) # Adjust top margin


    
    return fig_x, fig_y, fig_z, marker  

if __name__ == '__main__':
    app.run_server(debug=False)