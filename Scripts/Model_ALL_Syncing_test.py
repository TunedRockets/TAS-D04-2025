'''
This file deals with the syncing of data:
I.e. it takes in the unsynced data, and returns synced data. Do not actuallly import this file,
just use the functions in Handling_ALL_Functions.
authors: Johannes, CJ

'''

# External imports
import warnings
import pandas as pd
import numpy as np
import inspect
import matplotlib.pyplot as plt
import itertools

warnings.simplefilter(action='ignore', category=FutureWarning)

# Internal imports
import Handling_ALL_Functions
import constants

#######################################################################################################################
"""Functions for plotting processed data"""

def LT_x_plotter(tow):
    """
    This function visually shows the LT_xvelocity data and highlights the first time
    x reaches approximately 930 mm.
    """

    # Get LT x-position and time data
    LT_x = np.array(Handling_ALL_Functions.get_processed_data(tow, "LT")["x"])
    LT_time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LT")["time"])

    # Find the indeces where x is in the range [0, 1000]
    start_index = next((i for i, x in enumerate(LT_x) if 0 <= x <= 1000), None)

    for i in range(start_index, len(LT_x)):
        if not (0 <= LT_x[i] <= 1000):
            break
        end_index = i

    # Slice the data
    LT_x = LT_x[start_index:end_index + 1]
    LT_time = LT_time[start_index:end_index + 1]

    # Find the index where x is first near 930 mm in the sliced data
    target_x = 930   # mm
    tolerance = 0.5  # mm
    match_index = next((i for i, x in enumerate(LT_x) if abs(x - target_x) <= tolerance), None)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(LT_time, LT_x, label="X Position vs Time", color="blue")

    # If a matching point was found, plot a red dot and annotate it
    if match_index is not None:
        x_val = LT_x[match_index]
        time_val = LT_time[match_index]
        plt.plot(time_val, x_val, 'ro', label=f"x ≈ {target_x} mm")

    # Labels and legend
    plt.title("X Position vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("X Position [mm]")
    plt.legend()
    plt.grid(True)
    plt.show()

def LLS_A_plotter(tow):
    """
    This function visually shows the LLS A width data
    """

    # Get LLS A width and time data
    LLS_A_width = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_A")["width"])
    LLS_A_time = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_A")["time"])

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(LLS_A_time, LLS_A_width, label="LLS A Width vs Time", color="red")

    # Labels and legend
    plt.title("LLS A Width vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("LLS A Width [mm]")
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def LLS_B_plotter(tow):
    """
    This function visually shows the LLS B width data
    """

    # Get LLS B width and time data
    LLS_B_width = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_B")["width"])
    LLS_B_time = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_B")["time"])

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(LLS_B_time, LLS_B_width, label="LLS B Width vs Time", color="orange")

    # Labels and legend
    plt.title("LLS B Width vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("LLS B Width [mm]")
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def CAM_plotter(tow):
    """
    This function visually shows the CAM centerline data
    """

    # Get CAM centerline and time data
    CAM_center = Handling_ALL_Functions.get_processed_data(tow,"CAM")["center"]
    CAM_time = Handling_ALL_Functions.get_processed_data(tow,"CAM")["time"]

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(CAM_time, CAM_center, label="Camera centerline vs Time", color="green")

    # Labels and legend
    plt.title("Camera centerline vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("Camera centerline [mm]")
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def plot_all_processed_data(tow):
    """
    This function visually shows all of the processed data in one graph,
    including scaled LT X position (0 to 8 mm), LLS A width, LLS B width,
    and CAM centerline. A red dot marks the first time LT x ≈ 930 mm.
    """

    # Get all processed data
    LT_x = np.array(Handling_ALL_Functions.get_processed_data(tow, "LT")["x"])
    LT_time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LT")["time"])

    LLS_A_width = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_A")["width"])
    LLS_A_time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_A")["time"])

    LLS_B_width = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_B")["width"])
    LLS_B_time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_B")["time"])

    CAM_center = np.array(Handling_ALL_Functions.get_processed_data(tow, "CAM")["center"])
    CAM_time = np.array(Handling_ALL_Functions.get_processed_data(tow, "CAM")["time"])

    # Limit LT_x and LT_time to first segment where 0 <= x <= 1000
    start_index = next((i for i, x in enumerate(LT_x) if 0 <= x <= 1000), None)
    for i in range(start_index, len(LT_x)):
        if not (0 <= LT_x[i] <= 1000):
            break
        end_index = i

    LT_x_segment = LT_x[start_index:end_index + 1]
    LT_time_segment = LT_time[start_index:end_index + 1]
    LT_time_segment = LT_time_segment - LT_time_segment[0]

    # Scale LT_x to range 0–8 mm
    x_min = np.min(LT_x_segment)
    x_max = np.max(LT_x_segment)
    if x_max > x_min:
        LT_x_scaled = (LT_x_segment - x_min) / (x_max - x_min) * 8
    else:
        LT_x_scaled = np.zeros_like(LT_x_segment)  # avoid divide-by-zero if flat

    # Find first point near original x = 930 mm
    target_x = 930
    tolerance = 0.5
    match_index = next((i for i, x in enumerate(LT_x_segment) if abs(x - target_x) <= tolerance), None)

    # Plot all data on one graph
    plt.figure(figsize=(10, 6))
    plt.plot(LT_time_segment, LT_x_scaled, label="LT X Position (scaled to 0–8 mm)", color="blue")
    plt.plot(LLS_A_time, LLS_A_width, label="LLS A Width", color="red")
    plt.plot(LLS_B_time, LLS_B_width, label="LLS B Width", color="orange")
    plt.plot(CAM_time, CAM_center, label="CAM Centerline", color="green")

    # Add red dot at x ≈ 930 mm
    if match_index is not None:
        x_val_original = LT_x_segment[match_index]
        x_val_scaled = LT_x_scaled[match_index]
        time_val = LT_time_segment[match_index]
        plt.plot(time_val, x_val_scaled, 'ro')

    # Labels, title, legend
    plt.title("All Processed Data vs Time (LT x scaled to 0–8 mm)")
    plt.xlabel("Time [s]")
    plt.ylabel("Value [mm]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#######################################################################################################################
"""Functions for finding the sync needed for joining data"""

#######################################################################################################################

def main():
    tow = 2
    plot_all_processed_data(tow)

if __name__ == "__main__":
    main()