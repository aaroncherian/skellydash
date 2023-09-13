from dash import dcc, html
from plotting_utils import create_gauge_plot


def create_gauges_UI(rmse_values):
    return [
        dcc.Graph(figure=create_gauge_plot(rmse_values['total'], "Total RMSE"), style={'width': '25%'}),
        dcc.Graph(figure=create_gauge_plot(rmse_values['x'], "X RMSE"), style={'width': '25%'}),
        dcc.Graph(figure=create_gauge_plot(rmse_values['y'], "Y RMSE"), style={'width': '25%'}),
        dcc.Graph(figure=create_gauge_plot(rmse_values['z'], "Z RMSE"), style={'width': '25%'})
    ]

def create_total_rmse_indicator(rmse_values):
    return dcc.Graph(figure=create_gauge_plot(rmse_values['total'], "Total RMSE"), style={'width': '25%'})

def display_marker_list(marker_position_df):
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
        if (idx + 1) % 2 == 0:
            marker_list.append(html.Br())
    return marker_list