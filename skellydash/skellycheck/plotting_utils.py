import pandas as pd
import plotly.express as px
from dash import dcc
import plotly.graph_objects as go

def create_gauge_plot(value, title):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': 'blue'}}))
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=20))
    return fig

# Function to create a marker figure from a dataframe




def create_marker_figure_from_dataframe(dataframe_of_3d_data, ax_range=1200):
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

def subsample_and_create_figure(dataframe_of_3d_data, n=100):
        #downsample the data to make the 3D plot work faster (n is the downsampling factor)
        subsampled_df = dataframe_of_3d_data[dataframe_of_3d_data['frame'] % n == 0]
        marker_figure = create_marker_figure_from_dataframe(subsampled_df)

        return marker_figure
