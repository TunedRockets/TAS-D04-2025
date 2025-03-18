import numpy as np
import pandas as pd
import glob
import os

def get_directory_LLS_data(LLS_type, LLS_tow_number):
    """
    Generates the directory for the LLS data files as a function of the LLS type and the tow number
    """
    
    path_start = "Raw data\Data Sans Camera\LLS\Straight lines"
    path_extension = ".csv"
    path_number = "\\" + str(LLS_tow_number) + "\\" + "LLS_" + str(LLS_type) + "_data"
    directory = path_start + path_number + path_extension
    return(directory)

def get_LLS_timestamps(line_id:int)->list:
    """
    Gets the timestamps of the LLS data
    """

    # get the path (currently fixed path, so don't move stuff around)
    path_start = "Raw data\Data Sans Camera\LLS\Straight lines"
    path_extension = ".csv"
    path_number = "\\" + str(line_id) + "\\" + "LLS_A_B_profilenum_timestamp_data"
    path = path_start + path_number + path_extension

    # grab the data
    with open(path, "r") as file:
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].split(";") # splits the csv
    
    data_time_array = np.array(data)
    clean_LLS_time_data = np.delete(data_time_array, [1, 2, 3, 4, 5, 6], axis=1) #removes everything that is not a timestamp
    return clean_LLS_time_data #Returns an array of 1 column with timestamps

def load_LLS_data(LLS_type, LLS_tow_number):
    """
    For LLS type A: LLS_type = A_3060
    For LLS type B: LLS_type = B_3010
    """
    file_pattern = get_directory_LLS_data(LLS_type, LLS_tow_number) #Calls get_directory_LLS_data to generate the appropriate path
    #file_pattern = os.path.join(directory, f"LLS_{LLS_type}_data.csv")
    files = glob.glob(file_pattern)

    all_coords = []

    for file_path in files:
        data = pd.read_csv(file_path, header=None)

        # Skip the first row and filter rows with exactly 4096 values
        data = data.iloc[1:]  # Removing the first row
        valid_rows = data[data.apply(lambda row: len(row) == 4096, axis=1)]

        if valid_rows.empty:
            print(f"File {file_path} contains no valid rows with 4096 values. Skipping this file.")
            continue  # Skip files that have no valid rows

        for _, row in valid_rows.iterrows():
            values = row.to_numpy()

            # Split the row into y and z coordinates
            y_coords = values[:2048]
            z_coords = values[2048:]

            # Append the pair (y_coords, z_coords) as a tuple into the all_coords list
            all_coords.append((y_coords, z_coords))

    return np.array(all_coords, dtype=object)  # Returns a large array where each element is a tuple (y_coords, z_coords)

def connect_LLS_timestamps_to_data(clean_LLS_time_data, all_coords):
    """
    Stacks the timestamps column and the y and z coordinate columns next to each other and removes empty rows
    """
    LLS_data_with_zeros = np.hstack((clean_LLS_time_data, all_coords)) #Stacking the columns
    LLS_data = np.array([row for row in LLS_data_with_zeros if not any(coord == 0 for coord in row[1:])], dtype=object)
    return LLS_data

# Example usage:
# directory = "C:/Users/srott/PycharmProjects/TAS-D04-2025/Raw data/Data Sans Camera/LLS/Straight lines/1"
# coords_A = load_laser_data(directory, "A_3060")
# coords_B = load_laser_data(directory, "B_3010")
# print(coords_A)
# print(coords_B)
