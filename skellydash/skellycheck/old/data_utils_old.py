from pathlib import Path
import numpy as np
import pandas as pd
from convert_array_to_dataframe import mediapipe_markers, qualisys_markers
from marker_extraction import extract_specific_markers, markers_to_extract

# Load .npy data from a given file path
def load_npy_data(file_path):
    try:
        data = np.load(file_path)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File {file_path} not found.")

# Extract markers and convert 3D array data to a dataframe
def extract_and_convert_data(data, markers_list, markers_to_extract):
    extracted_data = extract_specific_markers(data_marker_dimension=data, list_of_markers=markers_list, markers_to_extract=markers_to_extract)
    dataframe = convert_3d_array_to_dataframe(data_3d_array=extracted_data, data_marker_list=markers_to_extract)
    return dataframe

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

# Main function to load and process mocap data
def load_and_process_data(path_to_freemocap_array, path_to_qualisys_array):
    # Load 3D data arrays
    freemocap_3d_data = load_npy_data(path_to_freemocap_array)
    qualisys_3d_data = load_npy_data(path_to_qualisys_array)
    
    # Check if data is loaded successfully
    if freemocap_3d_data is None or qualisys_3d_data is None:
        raise ValueError("Data could not be loaded.")

    # Extract markers and convert to dataframe
    freemocap_dataframe = extract_and_convert_data(freemocap_3d_data, mediapipe_markers, markers_to_extract)
    qualisys_dataframe = extract_and_convert_data(qualisys_3d_data, qualisys_markers, markers_to_extract)
    
    # Add system labels
    freemocap_dataframe['system'] = 'freemocap'
    qualisys_dataframe['system'] = 'qualisys'
    
    # Combine dataframes
    dataframe_of_3d_data = pd.concat([freemocap_dataframe, qualisys_dataframe], ignore_index=True)
    
    return dataframe_of_3d_data

def subsample_dataframe(dataframe, frame_skip_interval):
    """
    Subsample a DataFrame by selecting rows whose frame number is a multiple
    of the given subsample_factor.
    
    Parameters:
    - dataframe (pd.DataFrame): The DataFrame to be subsampled.
    - frame_skip_interval (int): The factor by which to subsample. 
                              For example, if frame_skip_interval = 3, every third frame will be kept.
                              
    Returns:
    - pd.DataFrame: The subsampled DataFrame.
    """
    
    # Use the modulo operator to find rows where the frame number is a multiple of subsample_factor
    subsampled_df = dataframe[dataframe['frame'] % frame_skip_interval == 0]
    
    return subsampled_df