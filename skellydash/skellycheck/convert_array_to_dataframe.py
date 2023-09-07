import pandas as pd
import numpy as np

def convert_3d_array_to_dataframe(data_3d_array:np.ndarray, data_marker_list:list):
    """
    Convert the FreeMoCap data from a numpy array to a pandas DataFrame.

    Parameters:
    - data_3d_array (numpy.ndarray): The 3d data array. Shape should be (num_frames, num_markers, 3).
    - data_marker_list (list): List of marker names 

    Returns:
    - data_frame_marker_dim_dataframe (pandas.DataFrame): DataFrame containing FreeMoCap data with columns ['Frame', 'Marker', 'X', 'Y', 'Z'].

    """
    num_frames = data_3d_array.shape[0]
    num_markers = data_3d_array.shape[1]

    frame_list = []
    marker_list = []
    x_list = []
    y_list = []
    z_list = []

    for frame in range(num_frames):
        for marker in range(num_markers):
            frame_list.append(frame)
            marker_list.append(data_marker_list[marker])
            x_list.append(data_3d_array[frame, marker, 0])
            y_list.append(data_3d_array[frame, marker, 1])
            z_list.append(data_3d_array[frame, marker, 2])

    data_frame_marker_dim_dataframe = pd.DataFrame({
        'frame': frame_list,
        'marker': marker_list,
        'x': x_list,
        'y': y_list,
        'z': z_list
    })

    return data_frame_marker_dim_dataframe



mediapipe_markers = ['nose',
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

qualisys_markers = [
'head',
'left_ear',
'right_ear',
'cspine',
'left_shoulder',
'right_shoulder',
'left_elbow',
'right_elbow',
'left_wrist',
'right_wrist',
'left_index',
'right_index',
'left_hip',
'right_hip',
'left_knee',
'right_knee',
'left_ankle',
'right_ankle',
'left_heel',
'right_heel',
'left_foot_index',
'right_foot_index',
]
