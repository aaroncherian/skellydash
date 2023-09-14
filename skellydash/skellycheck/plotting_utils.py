import plotly.express as px
from dash import dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

import pandas as pd

from plotly.tools import mpl_to_plotly
import matplotlib.pyplot as plt
import pandas as pd

import random

def create_gauge_plot(value, title):
    fig = go.Figure(go.Indicator(
        mode="number",
        value=value,
        title={'text': title},
        ))
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=20))
    return fig

# Function to create a marker figure from a dataframe




def create_3d_scatter_from_dataframe(dataframe_of_3d_data, ax_range=1200):
    x_mean = dataframe_of_3d_data["x"].mean()
    y_mean = dataframe_of_3d_data["y"].mean()
    z_mean = dataframe_of_3d_data["z"].mean()

    fig = px.scatter_3d(dataframe_of_3d_data, x="x", y="y", z="z", 
                        animation_frame="frame",
                        animation_group="marker",
                        color="system",
                        color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'},
                        hover_name="marker",
                        hover_data=["x", "y", "z"],
                        range_x=[x_mean - ax_range, x_mean + ax_range], 
                        range_y=[y_mean - ax_range, y_mean + ax_range],
                        range_z=[z_mean - ax_range, z_mean + ax_range]
    )
    fig.update_layout(
        scene_aspectmode='cube',
        autosize=False,
        height=1000,
        width=1100,
        margin={"t": 1, "b": 1, "l": 1, "r": 1},
    )
    return fig


def create_trajectory_plots(marker, dataframe_of_3d_data, color_of_cards):
    df_marker = dataframe_of_3d_data[dataframe_of_3d_data.marker == marker]
    
    trajectory_plot_height = 350
    # Your plotting code here. For demonstration, using placeholders.
    fig_x = px.line(df_marker, x='frame', y='x', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_y = px.line(df_marker, x='frame', y='y', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')
    fig_z = px.line(df_marker, x='frame', y='z', color='system', color_discrete_map={'freemocap': 'blue', 'qualisys': 'red'}, render_mode='svg')

    fig_x.update_xaxes(title_text='', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y.update_xaxes(title_text='', showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18))
    fig_y.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    # Return the list of Plotly figures
    return [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z)]



def create_rmse_bar_plot(df):
    dimensions = ['x_error', 'y_error', 'z_error']
    figures = {}
    
    for dim in dimensions:
        filtered_df = df[(df['dimension'] == 'Per Joint') & (df['coordinate'] == dim)]
        fig = go.Figure(data=[
            go.Bar(name=dim, x=filtered_df['marker'], y=filtered_df['RMSE'])
        ])
        fig.update_layout(
            title=f'RMSE for each marker ({dim})',
            xaxis_title='Marker',
            yaxis_title='RMSE Value'
        )
        figures[dim] = fig
    
    return figures


def create_error_plots(marker, absolute_error_dataframe, color_of_cards):
    df_marker = absolute_error_dataframe[absolute_error_dataframe.marker == marker]

    trajectory_plot_height = 500
    
    # Your plotting code for X, Y, and Z error over frames.
    fig_x = px.line(df_marker, x='frame', y='x_error', title='X Error over Time', render_mode='svg')
    fig_y = px.line(df_marker, x='frame', y='y_error', title='Y Error over Time', render_mode='svg')
    fig_z = px.line(df_marker, x='frame', y='z_error', title='Z Error over Time', render_mode='svg')
    
    fig_x.update_xaxes(title_text='', showticklabels=False)
    fig_x.update_yaxes(title_text='X', title_font=dict(size=18))
    fig_x.update_layout(paper_bgcolor=color_of_cards)

    fig_y.update_xaxes(title_text='', showticklabels=False)
    fig_y.update_yaxes(title_text='Y', title_font=dict(size=18))
    fig_y.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    fig_z.update_xaxes(title_text='Frame', title_font=dict(size=18))
    fig_z.update_yaxes(title_text='Z', title_font=dict(size=18))
    fig_z.update_layout(paper_bgcolor=color_of_cards, height=trajectory_plot_height)

    
    return [dcc.Graph(figure=fig_x), dcc.Graph(figure=fig_y), dcc.Graph(figure=fig_z)]

def find_continuous_segments(frames):
    segments = []
    start = frames[0]

    for i in range(1, len(frames)):
        if frames[i] != frames[i - 1] + 1:
            segments.append((start, frames[i - 1]))
            start = frames[i]

    segments.append((start, frames[-1]))

    return segments

def add_error_shapes(fig, frames, max_value, color):
    shapes = []
    for start, end in frames:
        shapes.append(dict(type="rect",
                x0=start - 0.5,
                x1=end + 0.5,
                y0=0,
                y1=max_value,
                fillcolor=color,
                opacity=0.2,
                layer="below",
                line_width=0,))
    return shapes

def create_error_shading_plots(marker, dataframe_of_3d_data, absolute_error_dataframe, color_of_cards):
    """
    Plot FreeMoCap trajectories for a specific marker with error shading.
    """

    # Pre-filter the DataFrames
    filtered_df = dataframe_of_3d_data.query("marker == @marker and system == 'freemocap'")
    filtered_error_df = absolute_error_dataframe.query("marker == @marker")

    graphs = []

    for dimension in ['x', 'y', 'z']:
        fig = go.Figure()

        high_error_frames = find_continuous_segments(filtered_error_df.query(f"{dimension}_error > 65")['frame'].tolist())
        low_error_frames = find_continuous_segments(filtered_error_df.query(f"{dimension}_error < 20")['frame'].tolist())

        bad_shapes = add_error_shapes(fig, high_error_frames, filtered_df[dimension].max(), "Red")
        good_shapes = add_error_shapes(fig, low_error_frames, filtered_df[dimension].max(), "Green")

        fig.add_trace(go.Scatter(x=filtered_df['frame'], y=filtered_df[dimension], mode='lines', name=f'{dimension.upper()} trajectory'))

        fig.update_layout(
            title=f'{dimension.upper()} Trajectory for {marker}',
            xaxis_title='Frame',
            yaxis_title='Position',
            xaxis=dict(showline=True, showgrid=False),
            yaxis=dict(showline=True, showgrid=False),
            paper_bgcolor=color_of_cards,
        )
        fig.update_layout(
            shapes=bad_shapes + good_shapes,
        )

        graphs.append(dcc.Graph(figure=fig))

    return graphs