# from dash import Dash, dcc, html, Input, Output, callback
# import plotly.graph_objs as go
# import numpy as np
# from pathlib import Path

# # Assuming you have your data loaded as a list of numpy arrays named 'data'
# # data[i] is the ith frame
# # data[i][j] is the jth marker on the ith frame
# # data[i][j][k] is the kth dimension of the jth marker on the ith frame
# path_to_numpy_array = Path(r"D:\2023-05-17_MDN_NIH_data\1.0_recordings\calib_3\sesh_2023-05-17_15_36_03_MDN_OneLeg_Trial1\output_data\mediapipe_body_3d_xyz.npy")
# data = np.load(path_to_numpy_array)

# import plotly.express as px
# df = px.data.gapminder()
# fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country",
#            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

# fig.show()

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
df["frame"] = np.repeat(np.arange(frames), markers)
df["marker"] = np.tile(np.arange(markers), frames)
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


fig2 = px.line_3d(df_connections, x="x", y="y", z="z",
                  animation_frame="frame",
                  line_group='connection',)


frames = [
    go.Frame(data=f.data + fig1.frames[i].data, name=f.name)
    for i, f in enumerate(fig2.frames)
]

fig_final = go.Figure(data=frames[0].data, frames=frames, layout=fig1.layout)

fig_final.show()