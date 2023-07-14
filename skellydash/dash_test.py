import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import json

from full_skeleton_graph import create_skeleton_figure
from pathlib import Path

import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

load_figure_template('SOLAR')

path_to_numpy_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_15_36_03_MDN_OneLeg_Trial1\output_data\mediapipe_body_3d_xyz.npy")

marker_figure, marker_position_df = create_skeleton_figure(path_to_numpy_array)

# create list of marker names
def display_marker_list():
    unique_markers = sorted(marker_position_df['marker'].unique())
    marker_list = []
    for idx, marker in enumerate(unique_markers):
        marker_list.append(
            html.Button(
                marker, 
                id={'type': 'marker-button', 'index': marker}, 
                className='btn btn-outline-primary', 
                style={'margin': '5px', 'width': '120px', 'height': 'px', 'padding': '2px', 'word-wrap': 'break-word'}
            )
        )
        # Insert a line break after each pair of markers to create two columns
        if (idx + 1) % 2 == 0:
            marker_list.append(html.Br())
    return marker_list

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Marker List", className="text-primary"),
            html.Div(id='marker-list', children=display_marker_list(), style={'display': 'flex', 'flexWrap': 'wrap'})], 
            md=1, style={'height': '100vh'}
        ),
        dbc.Col([
            html.H2("3D Scatter Plot", className="text-primary"),
            dcc.Graph(id='main-graph', figure=marker_figure)], 
            md=6, style={'height': '100vh'}
        ),
        dbc.Col(
            dbc.Container([
                html.H2("Marker Trajectory", className="text-primary"),
                html.H3(id='selected-marker', children="Select a marker", className="text-info"),
                dcc.Graph(id='x-trajectory'),
                dcc.Graph(id='y-trajectory'),
                dcc.Graph(id='z-trajectory'),
            ], style={'height': '100vh'}),
            md=5),
    ])
], fluid=True)


@app.callback(
    [Output('x-trajectory', 'figure'),
     Output('y-trajectory', 'figure'),
     Output('z-trajectory', 'figure'),
     Output('selected-marker', 'children'),
     Output({'type': 'marker-button', 'index': ALL}, 'className')],
    [Input('main-graph', 'clickData'),
     Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],
    [State('selected-marker', 'children'),
     State({'type': 'marker-button', 'index': ALL}, 'id')]
)
def display_trajectories(clickData, marker_clicks, selected_marker, button_ids):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update
    else:
        input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if 'marker-button' in input_id:
        marker = json.loads(input_id)['index']
    elif clickData is not None and 'points' in clickData and len(clickData['points']) > 0 and 'id' in clickData['points'][0]:
        marker = clickData['points'][0]['id']
    else:
        marker = selected_marker

    updated_classnames = []
    for button_id in button_ids:
        if button_id['index'] == marker:
            updated_classnames.append('btn btn-primary')
        else:
            updated_classnames.append('btn btn-outline-primary')

    df_marker = marker_position_df[marker_position_df.marker == marker]

    trajectory_plot_height = 350
    fig_x = px.line(df_marker, x='frame', y='x')
    fig_x.update_xaxes(title_text = '', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18, ))

    fig_y = px.line(df_marker, x='frame', y='y')
    fig_y.update_xaxes(title_text = '',showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18,))
    fig_y.update_layout(margin=dict(t=5), height = trajectory_plot_height)

    fig_z = px.line(df_marker, x='frame', y='z')
    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(margin=dict(t=5), height = trajectory_plot_height)

    return fig_x, fig_y, fig_z, marker, updated_classnames


if __name__ == '__main__':
    app.run_server(debug=False)
