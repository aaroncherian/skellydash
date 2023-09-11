from pathlib import Path
import numpy as np
import pandas as pd
from convert_array_to_dataframe import convert_3d_array_to_dataframe, mediapipe_markers, qualisys_markers
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
