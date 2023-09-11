
from pathlib import Path
import numpy as np
import pandas as pd

from convert_array_to_dataframe import convert_3d_array_to_dataframe, mediapipe_markers, qualisys_markers
from marker_extraction import extract_specific_markers, markers_to_extract
from marker_3d_graph import create_marker_figure_from_dataframe

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import json

import plotly.express as px
import plotly.graph_objects as go


def create_gauge(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': 'blue'}}))
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=20))
    return fig


path_to_freemocap_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_14_53_48_MDN_NIH_Trial3\output_data\mediapipe_body_3d_xyz_transformed.npy")
path_to_qualisys_array = r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\qualisys_MDN_NIH_Trial3\output_data\clipped_qualisys_skel_3d.npy"

freemocap_3d_data = np.load(path_to_freemocap_array)
qualisys_3d_data = np.load(path_to_qualisys_array)

freemocap_3d_data = freemocap_3d_data[0:10000, :, :]
qualisys_3d_data = qualisys_3d_data[0:10000, :, :]

freemocap_extracted_data = extract_specific_markers(data_marker_dimension=freemocap_3d_data, list_of_markers=mediapipe_markers, markers_to_extract=markers_to_extract)
qualisys_extracted_data = extract_specific_markers(data_marker_dimension=qualisys_3d_data, list_of_markers=qualisys_markers, markers_to_extract=markers_to_extract)

freemocap_dataframe = convert_3d_array_to_dataframe(data_3d_array=freemocap_extracted_data, data_marker_list=markers_to_extract)
qualisys_dataframe = convert_3d_array_to_dataframe(data_3d_array=qualisys_extracted_data, data_marker_list=markers_to_extract)

freemocap_dataframe['system'] = 'freemocap'
qualisys_dataframe['system'] = 'qualisys'

n = 100
dataframe_of_3d_data = pd.concat([freemocap_dataframe, qualisys_dataframe], ignore_index=True)
subsampled_df = dataframe_of_3d_data[dataframe_of_3d_data['frame'] % n == 0]


marker_figure = create_marker_figure_from_dataframe(subsampled_df)
marker_position_df = subsampled_df

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
load_figure_template('LUX')
color_of_cards = '#F3F5F7'

marker_figure.update_layout(paper_bgcolor=color_of_cards, plot_bgcolor=color_of_cards)

rmse_total = 20
rmse_x = 10
rmse_y = 5
rmse_z = 5

gauges = [
    dcc.Graph(figure=create_gauge(rmse_total, "Total RMSE"), style={'width': '25%'}),
    dcc.Graph(figure=create_gauge(rmse_x, "X RMSE"), style={'width': '25%'}),
    dcc.Graph(figure=create_gauge(rmse_y, "Y RMSE"), style={'width': '25%'}),
    dcc.Graph(figure=create_gauge(rmse_z, "Z RMSE"), style={'width': '25%'})
]


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
    ]),
    dbc.Row(
        dbc.Card([
            dbc.CardHeader(
                html.H2("RMSE", className="text-primary")
        ),
        dbc.CardBody([
            html.Div(id='rmse-gauges', children = gauges, style={'display': 'flex'}),
        ],
        )
    ])
    )
], fluid=True)


@app.callback(
        
    [Output('selected-marker', 'children'),
     Output({'type': 'marker-button', 'index': ALL}, 'className'),
     Output('trajectory-plots', 'children'),
     ],
    [Input('main-graph', 'clickData'),
     Input('main-graph', 'hoverData'),  # New Input for hoverData
     Input({'type': 'marker-button', 'index': ALL}, 'n_clicks')],
    [State('selected-marker', 'children'),
     State({'type': 'marker-button', 'index': ALL}, 'id')]
)
def display_trajectories(clickData, hoverData, marker_clicks, selected_marker, button_ids):
    
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
        elif hoverData is not None and 'points' in hoverData and len(hoverData['points']) > 0 and 'id' in hoverData['points'][0] and button_id['index'] == hoverData['points'][0]['id']: 
            updated_classnames.append('btn btn-info')  
        else:
            updated_classnames.append('btn btn-dark')
    trajectory_plot_height = 350

    df_marker = dataframe_of_3d_data[dataframe_of_3d_data.marker == marker]

    # Plotting for FreeMoCap and Qualisys
    fig_x = px.line(df_marker, x='frame', y='x', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'})
    fig_y = px.line(df_marker, x='frame', y='y', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'})
    fig_z = px.line(df_marker, x='frame', y='z', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'})

    # Further layout and style adjustments
    fig_x.update_xaxes(title_text='', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y.update_xaxes(title_text='', showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18))
    fig_y.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)


    return marker, updated_classnames, [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z)]


if __name__ == '__main__':
    app.run_server(debug=False)


