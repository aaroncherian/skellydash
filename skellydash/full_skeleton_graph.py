import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
from mediapipe_skeleton_builder import mediapipe_indices,mediapipe_connections,build_skeleton
import plotly.graph_objects as go
from rich.progress import track


def create_dataframe_for_bone_connections(skeleton_bones_list:list):
    """ Create a dataframe that lets you plot 'bones' for each frame of a skeleton.
        For each frame, each connection is listed with its 3d start and end coordinates.
    """
    data_frames = []
    for frame_num, frame in enumerate(skeleton_bones_list):
        for connection, points in frame.items():
            start_point, end_point = points
            for point_num, point in enumerate([start_point, end_point]):
                data_frames.append({
                    'frame': frame_num,
                    'connection': connection,
                    'point_num': point_num,  # 0 for start_point, 1 for end_point
                    'x': point[0],
                    'y': point[1],
                    'z': point[2]
                })

    bone_connections_df = pd.DataFrame(data_frames)

    return bone_connections_df

def create_dataframe_for_marker_positions(skeleton_3d_data:np.ndarray):
    frames, markers, dimensions = skeleton_3d_data.shape
    reshaped_data = np.reshape(skeleton_3d_data, (frames * markers, dimensions))
    marker_position_df = pd.DataFrame(reshaped_data, columns=["x", "y", "z"])

    marker_position_df["frame"] = np.repeat(np.arange(frames), markers) #creates the frame columns, and repeats the frame number for each marker
    marker_position_df["marker"] = np.tile(np.arange(markers), frames) #creates the marker column, and repeats the marker number for each frame   
    marker_position_df['marker'] = marker_position_df['marker'].apply(lambda x: mediapipe_indices[x]) #replace the marker number with the marker name

    return marker_position_df

def create_marker_figure(marker_position_df:pd.DataFrame):
    x_mean = marker_position_df["x"].mean()
    y_mean = marker_position_df["y"].mean()
    z_mean = marker_position_df["z"].mean()

    ax_range = 1200

    fig = px.scatter_3d(marker_position_df, x="x", y="y", z="z", 
                    animation_frame="frame", 
                    animation_group="marker",
                    hover_name="marker",
                    hover_data=["x", "y", "z"],
                    range_x=[x_mean - ax_range, x_mean + ax_range], 
                    range_y=[y_mean - ax_range, y_mean + ax_range],
                    range_z=[z_mean - ax_range, z_mean + ax_range],
    )
    fig.update_layout(
        scene_aspectmode='cube',
        autosize=False,
        height=1000,
        width=1100,
        margin={"t": 1, "b": 1, "l": 1, "r": 1},
    ) #keeps the ratio set
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000 / 30 #gives the animation a roughly 30fps framerate (speed is in ms)
    # go.Figure(layout=go.Layout(autosize=False, width=4000, height=4000))
    return fig

def create_bone_connections_figure(bone_connections_df:pd.DataFrame):
    connection_frames = []
    num_frames = bone_connections_df['frame'].nunique()
    
    connections = bone_connections_df['connection'].unique()

    # Creating a dictionary with connections as keys and sub-dataframes as values
    connection_dict = {connection: bone_connections_df[bone_connections_df['connection'] == connection] for connection in connections}
    
    # tqdm can wrap around any iterable
    for i in track(range(num_frames), description='Building connection frames: '):
        # Create an empty list to hold the traces for this frame
        traces = []

        # For each unique connection, create a trace
        for connection in connections:
            df_sub = connection_dict[connection][connection_dict[connection]['frame'] == i]
            trace = go.Scatter3d(
                x=df_sub['x'],
                y=df_sub['y'],
                z=df_sub['z'],
                mode='lines',
                hoverinfo='none',
                showlegend=False  # Disable hover for the lines
            )
            traces.append(trace)

        # Create the frame with the line traces for this frame
        frame = go.Frame(data=traces, name=i)
        connection_frames.append(frame)

    return connection_frames

def create_full_skeleton_frames(marker_frames, connection_frames):
    """ Combine the marker frames and connection frames into one list of frames
    """
    frames = []
    for i in track(range(len(connection_frames)), description="Creating full skeleton frames"):
        frame = go.Frame(data=list(connection_frames[i].data) + list(marker_frames[i].data), name=i)
        frames.append(frame)

    return frames

def create_skeleton_figure(path_to_numpy_array):

    data = np.load(path_to_numpy_array)

    data = data[:, :, :]

    mediapipe_skeleton = build_skeleton(data, mediapipe_indices, mediapipe_connections)

    bone_connections_df = create_dataframe_for_bone_connections(mediapipe_skeleton)
    marker_position_df = create_dataframe_for_marker_positions(data)

    marker_figure = create_marker_figure(marker_position_df)
    marker_frames = marker_figure.frames # Extract frames from the marker figure

    connection_frames = create_bone_connections_figure(bone_connections_df)

    full_skeleton_frames = create_full_skeleton_frames(marker_frames, connection_frames)

    # Create the final figure
    fig_final = go.Figure(data=full_skeleton_frames[0].data, frames=full_skeleton_frames, layout=marker_figure.layout)

    return fig_final, marker_position_df
    # fig_final.write_html(r'C:\Users\aaron\FreeMocap_Data\recording_sessions\test.html', include_plotlyjs='cdn')
    # fig_final.show()


