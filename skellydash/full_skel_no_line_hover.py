
mediapipe_indices = ['nose',
    'left_eye_inner',
    'left_eye',
    'left_eye_outer',
    'right_eye_inner',
    'right_eye',
    'right_eye_outer',
    'left_ear',
    'right_ear',
    'mouth_left',
    'mouth_right',
    'left_shoulder',
    'right_shoulder',
    'left_elbow',
    'right_elbow',
    'left_wrist',
    'right_wrist',
    'left_pinky',
    'right_pinky',
    'left_index',
    'right_index',
    'left_thumb',
    'right_thumb',
    'left_hip',
    'right_hip',
    'left_knee',
    'right_knee',
    'left_ankle',
    'right_ankle',
    'left_heel',
    'right_heel',
    'left_foot_index',
    'right_foot_index']

import plotly.express as px
import pandas as pd
import numpy as np
from pathlib import Path
from mediapipe_skeleton_builder import mediapipe_indices,mediapipe_connections,build_skeleton
import plotly.graph_objects as go

path_to_numpy_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_15_36_03_MDN_OneLeg_Trial1\output_data\mediapipe_body_3d_xyz.npy")
data = np.load(path_to_numpy_array)

data = data[1000:1200, :, :]

mediapipe_skeleton = build_skeleton(data, mediapipe_indices, mediapipe_connections)

data_frames = []
for frame_num, frame in enumerate(mediapipe_skeleton):
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

df_connections = pd.DataFrame(data_frames)


x_mean = np.mean(data[:, :, 0])
y_mean = np.mean(data[:, :, 1])
z_mean = np.mean(data[:, :, 2])

ax_range = 1500

frames, markers, dimensions = data.shape
reshaped_data = np.reshape(data, (frames * markers, dimensions))

df = pd.DataFrame(reshaped_data, columns=["x", "y", "z"])

# Add the frame and marker columns
df["frame"] = np.repeat(np.arange(frames), markers) #creates the frame columns, and repeats the frame number for each marker
df["marker"] = np.tile(np.arange(markers), frames) #creates the marker column, and repeats the marker number for each frame    
df['marker'] = df['marker'].apply(lambda x: mediapipe_indices[x])

# Use plotly.express to create the animated scatter plot
fig1 = px.scatter_3d(df, x="x", y="y", z="z", 
                    animation_frame="frame", 
                    animation_group="marker",
                    hover_name="marker",
                    hover_data=["x", "y", "z"],
                    range_x=[x_mean - ax_range, x_mean + ax_range], 
                    range_y=[y_mean - ax_range, y_mean + ax_range],
                    range_z=[z_mean - ax_range, z_mean + ax_range]
)
fig1.update_layout(scene_aspectmode='cube')
fig1.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000 / 30


frames = []

# For each frame in fig1 (which is based on the markers)
for i in range(len(fig1.frames)):
    # Create an empty list to hold the traces for this frame
    traces = []

    # For each unique connection, create a trace
    for connection in df_connections['connection'].unique():
        df_sub = df_connections[(df_connections['connection'] == connection) & (df_connections['frame'] == i)]
        trace = go.Scatter3d(
            x=df_sub['x'],
            y=df_sub['y'],
            z=df_sub['z'],
            mode='lines',
            hoverinfo='none',
            showlegend=False  # Disable hover for the lines
        )
        traces.append(trace)

    # Create the frame with the scatter and line traces for this frame
    frame = go.Frame(data=list(traces) + list(fig1.frames[i].data), name=i)
    frames.append(frame)

# Create the final figure
fig_final = go.Figure(data=frames[0].data, frames=frames, layout=fig1.layout)

fig_final.show()
