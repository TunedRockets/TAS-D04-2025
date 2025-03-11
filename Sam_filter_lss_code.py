import numpy as np
import pandas as pd
import glob
import os


def load_laser_data(directory, laser_type):
    """
    For laser type A: laser_type = A_3060
    For laser type B: laser_type = B_3010
    """
    file_pattern = os.path.join(directory, f"LLS_{laser_type}_data.csv")
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


# Example usage:
# directory = "C:/Users/srott/PycharmProjects/TAS-D04-2025/Raw data/Data Sans Camera/LLS/Straight lines/1"
# coords_A = load_laser_data(directory, "A_3060")
# coords_B = load_laser_data(directory, "B_3010")
# print(coords_A)
# print(coords_B)
