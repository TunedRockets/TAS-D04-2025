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

# UPDATE THE VELOCITY PLOTTER SYNCS TO THE NEW WAY OF FINDING THE SYNCS

def LT_x_plotter(tow):
    """
    This function visually shows the LT_x position data and highlights the first time
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

def LT_x_velocity_plotter(tow, sync=True):
    """
    This function visually shows the LT_x velocity data and highlights the first time
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
    LT_x = LT_x[start_index - 1:end_index + 1]
    LT_time = LT_time[start_index - 1 :end_index + 1]

    # Calculate the LT x velocity
    LT_x_velocity = []
    for i in range(1, len(LT_time)):
        x_velocity = (LT_x[i] - LT_x[i-1]) / (LT_time[i] - LT_time[i-1])
        LT_x_velocity.append(x_velocity)
    LT_x_velocity.append(x_velocity) # Append the last value twice to maintain consistency between array sizes
    LT_x_velocity = np.array(LT_x_velocity)
    
    # Find the index where x is first near 930 mm in the sliced data
    target_x = 930   # mm
    tolerance = 0.5  # mm
    match_index = next((i for i, x in enumerate(LT_x) if abs(x - target_x) <= tolerance), None)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(LT_time, LT_x_velocity, label="X Velocity vs Time", color="blue")

    # If a matching point was found, plot a red dot and annotate it
    if match_index is not None and sync is True:
        x__velocity_val = LT_x_velocity[match_index]
        time_val = LT_time[match_index]
        plt.plot(time_val, x__velocity_val, 'ro', label=f"x ≈ {target_x} mm")

    # Labels and legend
    plt.title("X Velocity vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("X Velocity [mm/s]")
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

def LLS_A_velocity_plotter(tow, sync=True):
    """
    This function visually shows the LLS A width velocity data
    """

    # Get LLS A width and time data
    LLS_A_width = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_A")["width"])
    LLS_A_time = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_A")["time"])

   # Calculate the LLS A width velocity
    LLS_A_width_velocity = []
    for i in range(1, len(LLS_A_time)):
        width_velocity = (LLS_A_width[i] - LLS_A_width[i-1]) / (LLS_A_time[i] - LLS_A_time[i-1])
        LLS_A_width_velocity.append(width_velocity)
    LLS_A_width_velocity.append(width_velocity) # Append the last value twice to maintain consistency between array sizes
    LLS_A_width_velocity = np.array(LLS_A_width_velocity)
    if sync:
        LLS_A_width_velocity = np.abs(LLS_A_width_velocity)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(LLS_A_time, LLS_A_width_velocity, label="LLS A Width Velocity vs Time", color="red")

    if sync:
        sync_index, sync_time = scan_for_min(
            window_duration=0.3,  
            time_array=LLS_A_time,
            value_array=LLS_A_width_velocity,
            search_start_time=4,
            search_end_time=5.3)
        plt.plot(LLS_A_time[sync_index], LLS_A_width_velocity[sync_index], 'ro', color="blue", label="Sync Point")

    # Labels and legend
    plt.title("LLS A Width Velocity vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("LLS A Width Velocity [mm/s]")
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

def LLS_B_velocity_plotter(tow, sync=True):
    """
    This function visually shows the LLS B width velocity data
    """

    # Get LLS B width and time data
    LLS_B_width = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_B")["width"])
    LLS_B_time = np.array(Handling_ALL_Functions.get_processed_data(tow,"LLS_B")["time"])

    # Calculate the LLS B width velocity
    LLS_B_width_velocity = []
    for i in range(1, len(LLS_B_time)):
        width_velocity = (LLS_B_width[i] - LLS_B_width[i-1]) / (LLS_B_time[i] - LLS_B_time[i-1])
        LLS_B_width_velocity.append(width_velocity)
    LLS_B_width_velocity.append(width_velocity) # Append the last value twice to maintain consistency between array sizes
    LLS_B_width_velocity = np.array(LLS_B_width_velocity)
    if sync:
        LLS_B_width_velocity = np.abs(LLS_B_width_velocity)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(LLS_B_time, LLS_B_width_velocity, label="LLS B Width Velocity vs Time", color="orange")

    if sync:
        sync_index, sync_time = scan_for_min(
            window_duration=0.3,  
            time_array=LLS_B_time,
            value_array=LLS_B_width_velocity,
            search_start_time=LLS_B_time[0],
            search_end_time=LLS_B_time[-1])
        plt.plot(LLS_B_time[sync_index], LLS_B_width_velocity[sync_index], 'ro', color="blue", label="Sync Point")

    # Labels and legend
    plt.title("LLS B Width Velocity vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("LLS B Width Velocity [mm/s]")
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def CAM_plotter(tow):
    """
    This function visually shows the CAM centerline data
    """

    # Get CAM centerline and time data
    CAM_center = np.array(Handling_ALL_Functions.get_processed_data(tow,"CAM")["center"])
    CAM_time = np.array(Handling_ALL_Functions.get_processed_data(tow,"CAM")["time"])

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

def CAM_velocity_plotter(tow, sync=True):
    """
    This function visually shows the CAM centerline velocity data
    """

    # Get CAM centerline and time data
    CAM_center = np.array(Handling_ALL_Functions.get_processed_data(tow,"CAM")["center"])
    CAM_time = np.array(Handling_ALL_Functions.get_processed_data(tow,"CAM")["time"])

    # Calculate the CAM centerline velocity
    CAM_center_velocity = []
    for i in range(1, len(CAM_time)):
        center_velocity = (CAM_center[i] - CAM_center[i-1]) / (CAM_time[i] - CAM_time[i-1])
        CAM_center_velocity.append(center_velocity)
    CAM_center_velocity.append(center_velocity) # Append the last value twice to maintain consistency between array sizes
    CAM_center_velocity = np.array(CAM_center_velocity)
    if sync:
        CAM_center_velocity = np.abs(CAM_center_velocity)

    # Plot the data
    plt.figure(figsize=(8, 5))
    plt.plot(CAM_time, CAM_center_velocity, label="Camera centerline velocity vs Time", color="green")

    if sync:
        sync_index, sync_time = scan_for_min(
            window_duration=0.3,
            time_array=CAM_time,
            value_array=CAM_center_velocity,
            search_start_time=CAM_time[0],
            search_end_time=CAM_time[-1])
        plt.plot(CAM_time[sync_index], CAM_center_velocity[sync_index], 'ro', color="blue", label="Sync Point")

    # Labels and legend
    plt.title("Camera centerline velocity vs Time")
    plt.xlabel("Time [s]")
    plt.ylabel("Camera centerline velocity [mm/s]")
    plt.legend()
    plt.grid(True)
    plt.show()
    return

def plot_all_processed_data(tow, synced=False):
    """
    This function visually shows all of the processed data in one graph,
    including scaled LT X position and velocity (0 to 8 mm), LLS A width, LLS B width,
    and CAM centerline. A red dot marks the first time LT x ≈ 930 mm.
    If `synced=True`, vertical dashed lines show synchronization times from all 4 data streams.
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
    LT_x_scaled = (LT_x_segment - x_min) / (x_max - x_min) * 8 if x_max > x_min else np.zeros_like(LT_x_segment)

    # Calculate and scale LT x velocity
    LT_x_velocity_segment = np.diff(LT_x_segment) / np.diff(LT_time_segment)
    LT_x_velocity_segment = np.append(LT_x_velocity_segment, LT_x_velocity_segment[-1])  # match lengths
    v_min = np.min(LT_x_velocity_segment)
    v_max = np.max(LT_x_velocity_segment)
    LT_x_velocity_scaled = (LT_x_velocity_segment - v_min) / (v_max - v_min) * 8 if v_max > v_min else np.zeros_like(LT_x_velocity_segment)

    # Find first point near x = 930 mm
    target_x = 930
    tolerance = 0.5
    match_index = next((i for i, x in enumerate(LT_x_segment) if abs(x - target_x) <= tolerance), None)

    # Plot all data
    plt.figure(figsize=(10, 6))
    plt.plot(LT_time_segment, LT_x_scaled, label="LT X Position (scaled 0–8 mm)", color="blue")
    plt.plot(LT_time_segment, LT_x_velocity_scaled, label="LT X Velocity (scaled 0–8 mm)", color="purple")
    plt.plot(LLS_A_time, LLS_A_width, label="LLS A Width", color="red")
    plt.plot(LLS_B_time, LLS_B_width, label="LLS B Width", color="orange")
    plt.plot(CAM_time, CAM_center, label="CAM Centerline", color="green")

    # Mark x ≈ 930 mm with red dot
    if match_index is not None:
        time_val = LT_time_segment[match_index]
        plt.plot(time_val, LT_x_scaled[match_index], 'ro')
        plt.plot(time_val, LT_x_velocity_scaled[match_index], 'ro')

    # If synced, mark the 4 sync times with dashed lines
    if synced:
        try:
            sync_LT = LT_sync(tow)
            sync_LLS_A = LLS_A_sync(tow)
            sync_LLS_B = LLS_B_sync(tow)
            sync_CAM = CAM_sync(tow)

            plt.axvline(sync_LT - LT_time[start_index], color="blue", linestyle="--", label="LT Sync")
            plt.axvline(sync_LLS_A, color="red", linestyle="--", label="LLS A Sync")
            plt.axvline(sync_LLS_B, color="orange", linestyle="--", label="LLS B Sync")
            plt.axvline(sync_CAM, color="green", linestyle="--", label="CAM Sync")

        except Exception as e:
            print(f"Sync failed: {e}")

    # Final labels and formatting
    plt.title("All Processed Data vs Time (LT x and velocity scaled to 0–8 mm)")
    plt.xlabel("Time [s]")
    plt.ylabel("Value [mm]")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#######################################################################################################################
"""Functions for finding the time sync of the different sensors"""

def scan_for_min(window_duration: float, time_array: np.ndarray, value_array: np.ndarray, search_start_time: float, search_end_time: float) -> tuple:
    """
    Finds the start index and time where the sum of squared values is minimized
    over a time window of fixed duration within a specified search time range.

    Parameters:
        window_duration (float): Duration of the time window to evaluate.
        time_array (np.ndarray): 1D array of time stamps (must be sorted).
        value_array (np.ndarray): 1D array of corresponding values.
        search_start_time (float): Start time of the search interval.
        search_end_time (float): End time of the search interval.

    Returns:
        tuple: (start_index, start_time) of the window with the minimum squared sum.
    """
    if search_end_time - search_start_time < window_duration:
        raise ValueError(
            f"Search interval too short: {search_end_time - search_start_time:.2f}s "
            f"(required ≥ {window_duration:.2f}s)")

    # Identify all valid starting indices within the search range
    valid_start_mask = (time_array >= search_start_time) & (time_array <= search_end_time - window_duration)
    valid_start_indices = np.where(valid_start_mask)[0]

    if len(valid_start_indices) == 0:
        raise ValueError("No valid start times found within the specified time range.")

    min_squared_sum = float('inf')
    min_sum_start_index = -1

    for start_index in valid_start_indices:
        window_end_time = time_array[start_index] + window_duration

        # Find the end index such that time stays within the window
        end_index = start_index
        while end_index < len(time_array) and time_array[end_index] <= window_end_time:
            end_index += 1

        squared_sum = np.sum(value_array[start_index:end_index] ** 2)

        if squared_sum < min_squared_sum:
            min_squared_sum = squared_sum
            min_sum_start_index = start_index

    if min_sum_start_index == -1:
        raise ValueError("No valid time window found within the specified range.")

    return min_sum_start_index, time_array[min_sum_start_index]

def LT_sync():
    """
    Finds the time when each of the 30 tows reaches x ≈ 930 mm,
    syncs all tows in time to match tow 2 at that point,
    and plots all LT velocity vs synced time curves with sync points marked.

    Returns the LT sync time of tow 2 and all tows' LT data synced in an array formated as
    [reference time | position data (30 cols) | velocity data (30 cols)].
    """

    target_x = 930
    tolerance = 0.2

    def get_cut_LT_data(tow):
        LT_x = np.array(Handling_ALL_Functions.get_processed_data(tow, "LT")["x"])
        LT_time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LT")["time"])

        # Get segment where 0 <= x <= 1000
        start_index = next((i for i, x in enumerate(LT_x) if 0 <= x <= 1000), None)
        for i in range(start_index, len(LT_x)):
            if not (0 <= LT_x[i] <= 1000):
                break
            end_index = i

        LT_x_segment = LT_x[start_index:end_index + 1]
        LT_time_segment = LT_time[start_index:end_index + 1]

        return LT_x_segment, LT_time_segment

    def get_LT_sync_time(tow):
        LT_x, LT_time = get_cut_LT_data(tow)
        match_index = next((i for i, x in enumerate(LT_x) if abs(x - target_x) <= tolerance), None)
        if match_index is None:
            raise ValueError(f"No x ≈ 930 mm found for tow {tow}")
        return LT_time[match_index]

    def compute_velocity(x, t):
        velocity = np.zeros_like(x)
        velocity[0] = 0  # or np.nan
        for i in range(1, len(x)):
            dt = t[i] - t[i - 1]
            if dt == 0:
                velocity[i] = 0  # Avoid division by zero
            else:
                velocity[i] = (x[i] - x[i - 1]) / dt
        return velocity

    # Get sync time of tow 2
    tow2_sync_time = get_LT_sync_time(2)

    plt.figure(figsize=(12, 6))

    # Initialize containers
    all_synced_times = []
    all_synced_positions = []
    all_synced_velocities = []

    for tow in range(2, 32):
        LT_x, LT_time = get_cut_LT_data(tow)
        sync_time = get_LT_sync_time(tow)

        synced_time = LT_time - (sync_time - tow2_sync_time)
        LT_velocity = compute_velocity(LT_x, LT_time)

        # Plot
        plt.plot(synced_time, LT_velocity, label=f"Tow {tow}")

        # Save synced data
        all_synced_times.append(synced_time)
        all_synced_positions.append(LT_x)
        all_synced_velocities.append(LT_velocity)

        # Draw vertical line at sync point (aligned to 930 mm)
        sync_point_aligned_time = tow2_sync_time
        plt.axvline(x=sync_point_aligned_time, color='gray', linestyle='--', alpha=0.2)

    # Plot styling
    plt.title("LT Velocity vs Synced Time (All Tows Aligned to Tow 2 at x ≈ 930 mm)")
    plt.xlabel("Synced Time [s]")
    plt.ylabel("LT Velocity [mm/s]")
    plt.grid(True)
    plt.tight_layout()
    plt.legend(fontsize="x-small", ncol=3)
    plt.show()

    # Use tow 2's time vector as the reference
    reference_time = all_synced_times[0]

    position_columns = []
    velocity_columns = []

    for i in range(30):  # Tow 2 to Tow 31
        pos_interp = np.interp(reference_time, all_synced_times[i], all_synced_positions[i])
        vel_interp = np.interp(reference_time, all_synced_times[i], all_synced_velocities[i])
        position_columns.append(pos_interp)
        velocity_columns.append(vel_interp)

    # Final data: [time | positions (30 cols) | velocities (30 cols)]
    synced_data_array = np.column_stack([reference_time] + position_columns + velocity_columns)

    return tow2_sync_time, synced_data_array

def LLS_A_sync(tow):
    """
    Find the time where the LLS A width velocity has a minimum squared sum
    in a 0.5s window between 4s and 6s.
    """
    width = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_A")["width"])
    time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_A")["time"])

    # Compute width velocity
    width_velocity = np.diff(width) / np.diff(time)
    width_velocity = np.append(width_velocity, width_velocity[-1])  # match lengths

    dummy_variable, sync_time = scan_for_min(
        window_duration=0.5,
        time_array=time,
        value_array=width_velocity,
        search_start_time=4.0,
        search_end_time=5.0)
    
    return sync_time

def LLS_B_sync(tow):
    """
    Find the time where the LLS B width velocity has a minimum squared sum
    in a 0.5s window between 4s and 6s.
    """
    width = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_B")["width"])
    time = np.array(Handling_ALL_Functions.get_processed_data(tow, "LLS_B")["time"])

    # Compute width velocity
    width_velocity = np.diff(width) / np.diff(time)
    width_velocity = np.append(width_velocity, width_velocity[-1])  # match lengths

    dummy_variable, sync_time = scan_for_min(
        window_duration=0.5,
        time_array=time,
        value_array=width_velocity,
        search_start_time=4.0,
        search_end_time=5.0)
    
    return sync_time

def CAM_sync(tow):
    """
    Find the time where the CAM centerline velocity has a minimum squared sum
    in a 0.5s window between 4s and 6s.
    """
    center = np.array(Handling_ALL_Functions.get_processed_data(tow, "CAM")["center"])
    time = np.array(Handling_ALL_Functions.get_processed_data(tow, "CAM")["time"])

    # Compute centerline velocity
    center_velocity = np.diff(center) / np.diff(time)
    center_velocity = np.append(center_velocity, center_velocity[-1])  # match lengths

    dummy_variable, sync_time = scan_for_min(
        window_duration=0.3,
        time_array=time,
        value_array=center_velocity,
        search_start_time=5.0,
        search_end_time=6.0)
    
    return sync_time

#######################################################################################################################

def main():
    # tow = 2
    dummy_variable, synced_LT_array = LT_sync()
    print(synced_LT_array)
    # plot_all_processed_data(tow, True)

if __name__ == "__main__":
    main()