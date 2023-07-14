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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

load_figure_template('LUX')

path_to_numpy_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_15_36_03_MDN_OneLeg_Trial1\output_data\mediapipe_body_3d_xyz.npy")
color_of_cards = '#F3F5F7'

marker_figure, marker_position_df = create_skeleton_figure(path_to_numpy_array)


marker_figure.update_layout(paper_bgcolor=color_of_cards, plot_bgcolor=color_of_cards)


# create list of marker names
def display_marker_list():
    unique_markers = sorted(marker_position_df['marker'].unique())
    marker_list = []
    for idx, marker in enumerate(unique_markers):
        marker_list.append(
            html.Button(
                marker, 
                id={'type': 'marker-button', 'index': marker}, 
                className='btn btn-dark', 
                style={'margin': '5px', 'width': '140px', 'height': '40px', 'padding': '2px', 'word-wrap': 'break-word'}
            )
        )
        # Insert a line break after each pair of markers to create two columns
        if (idx + 1) % 2 == 0:
            marker_list.append(html.Br())
    return marker_list

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H2("3D Scatter Plot", className="text-primary"),
                    className="text-primary"
                ),
                dbc.CardBody([
                    dcc.Graph(id='main-graph', figure=marker_figure),
                ],
                style={"backgroundColor": color_of_cards}
                )
            ], className="mb-4 mt-4"),
            dbc.Card([
                dbc.CardHeader(
                    html.H2("Marker List", className = "text-primary")
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Div(id='marker-list', 
                                     children=display_marker_list(), 
                                     style={'display': 'flex', 'flexWrap': 'wrap'})
                        ])
                    ])
                ])
            ], style={"backgroundColor": color_of_cards}, className="mb-4")  # Updated line
        ], md=6, style={'height': '100vh'}),
        dbc.Col(
            dbc.Container([
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Marker Trajectory", className="text-primary")
                    ),
                    dbc.CardBody([
                        html.H3(id='selected-marker', children="Select a marker", className="text-info"),
                        html.Div(id='trajectory-plots')  # This Div will contain the plots
                    ],
                    style={"backgroundColor": color_of_cards}
                    )
                ],
                className="mb-4 mt-4"
                )
            ], style={'height': '100vh'}),
            md=5
        )
    ])
], fluid=True)


@app.callback(
    [Output('selected-marker', 'children'),
     Output({'type': 'marker-button', 'index': ALL}, 'className'),
     Output('trajectory-plots', 'children')],  # We added this line
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
            updated_classnames.append('btn btn-warning')
        else:
            updated_classnames.append('btn btn-dark')

    df_marker = marker_position_df[marker_position_df.marker == marker]

    if df_marker.empty:
        return marker, updated_classnames, None

    trajectory_plot_height = 350
    fig_x = px.line(df_marker, x='frame', y='x')
    fig_x.update_xaxes(title_text = '', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18, ))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y = px.line(df_marker, x='frame', y='y')
    fig_y.update_xaxes(title_text = '',showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18,))
    fig_y.update_layout(margin=dict(t=5), paper_bgcolor=color_of_cards, height = trajectory_plot_height)

    fig_z = px.line(df_marker, x='frame', y='z')
    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(margin=dict(t=5), paper_bgcolor=color_of_cards, height = trajectory_plot_height)

    return marker, updated_classnames, [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z)]

if __name__ == '__main__':
    app.run_server(debug=False)
