

import Handling_ALL_Functions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

def join_data(frame1:pd.DataFrame, frame2:pd.DataFrame, shift:float)-> pd.DataFrame:
    '''
    joins the two dataframe columnwise from a given desync time\n
    I.e. shifts frame two BACKWARDS by the desync.\n
    assumes time is at index 0 in the columns\n
    (also needs both frames to have a column called "time")\n
    otherwise it breaks
    '''
    # PREPROCCESING:

    # shifting the 2nd frame before the process starts:
    frame2["time"] -= shift # numpy vectorization to the rescue

    # find the range of overlap between the data
    range_1 = min(frame1["time"]), max(frame1["time"])
    range_2 = min(frame2["time"]), max(frame2["time"])
    range_total = max(range_1[0],range_2[0]), min(range_1[1],range_2[1])
    if range_total[0] >= range_total[1]:
        raise IndexError("There is no overlap between the data")
    
    # find the indexes to get rid of and truncate:
    start_index_1 = frame1[frame1['time'].gt(range_total[0])].index[0]
    start_index_2 = frame2[frame2['time'].gt(range_total[0])].index[0]
    end_index_1 = frame1[frame1['time'].ge(range_total[1])].index[0]
    end_index_2 = frame2[frame2['time'].ge(range_total[1])].index[0]
    frame1 = frame1.truncate(start_index_1,end_index_1)
    frame2 = frame2.truncate(start_index_2,end_index_2)

    # info on frames
    shape_1 = frame1.shape
    shape_2 = frame2.shape

    # the shape of the joined is going to be the min of the row and the combined of the columns
    # minus one because time is shared
    columns = shape_1[1] + shape_2[1] - 1
    rows = min(shape_1[0], shape_2[0])

    # PROCESSING:
    joined = np.zeros((rows, columns))
    #set which frame is the guiding one:
    if shape_1[0] > shape_2[0]: # guiding is which one that guides the join process
        guide = frame2
        follower = frame1
    else:
        guide = frame1
        follower = frame2 # python is by reference so this shouldn't be slow
    
    try:
        i_f = 0 # follower index
        for i in range(len(guide)):
            # combine them 
            time = guide.iloc[i][0] # the time of the timestamp

            # put in guide data
            for j in range(0, guide.shape[1]):
                joined[i][j] = guide.iloc[i][j]

            # now find the corresponding data in the follower
            while follower.iloc[i_f][0] < time: # TODO, set this to closest, not just first above
                i_f += 1
                # might break if index goes out of range...
            # continues until it's passed the right point.
            # i_f is now at the follower just beyond the time data

            if abs(follower.iloc[i_f-1][0] - time) < abs(follower.iloc[i_f][0] - time):
                i_f -= 1
            # picks the closest one


            for j in range(1, follower.shape[1]):
                data_debug = follower.iloc[i_f][j]
                join_index = j + guide.shape[1] - 1 # -1 due to the time being removed
                joined[i][join_index] = data_debug  # puts it in the row after the guide
    except IndexError:
        # we probably ran out of datapoints in the follower :(
        # but that's fine
        # just remove the last line
        joined = joined[:-1,:]

    joined = pd.DataFrame(joined)
    # gets rid of the metadata, so let's reintroduce it
    fol_col_names = list(follower.columns)
    guide_col_names = list(guide.columns)
    col_names = ['time'] + guide_col_names[1:] + fol_col_names[1:]
    # combines them (and excludes first column which is time)


    # if not then change this
    joined.columns = col_names  


    return joined

def _test_join_function():
    '''just a function to test that joining works correctly'''
     # testing the shifting thing
    f1 = lambda x: np.exp(-(3*(x-2))**2/2.) # gaussian curve from ANA
    f2 = lambda x: 2*f1(x-1) # bigger curve shifted by 1

    xx1 = np.linspace(0,3,100) 
    xx2 = np.linspace(2,6,75)
    yy1 = f1(xx1)
    yy2 = f2(xx2)

    data1 = pd.DataFrame(np.array([xx1,yy1]).T)
    data2 = pd.DataFrame(np.array([xx2,yy2]).T)
    data1.columns = ["time", "value"]
    data2.columns = ["time", "shifted"]
    
    # plot the different data:
    # plt.plot(data1["time"],data1["value"])
    # plt.plot(data2["time"],data2["shifted"])
    # plt.show()

    # now try shifting

    combined = join_data(data1,data2,1)
    print(combined)
    plt.plot(combined["time"],combined["value"])
    plt.plot(combined["time"],combined["shifted"])
    plt.show()


def blue_dot_LT(tow:int, overwrite:bool=False):
    '''gets the time at where the LT is 930'''
    LT_x = Handling_ALL_Functions.get_processed_data(tow, "LT")["x"]
    LT_time = Handling_ALL_Functions.get_processed_data(tow, "LT")["time"]
    xi, _ = find_x930(LT_x, LT_time)
    index = LT_x.index(xi)
    return LT_time(index)




def find_x930(LT_x: list, LT_time: list):
    """This function grabs a sample of the LT data where we know the tape is being layed down
        and then calculates the distance between consective data points. Once the minimum
        distance between data points has been found in the sample, then for data points after
        the sample, if the distance between them is smaller than some factor beta times the minimum
        distance found in the sample, then we know that the tape has been cut and xi = 930mm.
        Then the coressponding time at xi is ti and this time can be used to sync the LT data with
        other data sets"""

    beta = 2
    delta_x_values = []
    x_values = []

    for i in range(int(len(LT_x)*0.45), int(len(LT_x)*0.48)):
        delta_x = (LT_x[i+1] - LT_x[i])/0.010 # Divided by the rate at which the LT scans
        x = LT_x[i]
        delta_x_values.append(delta_x)
        x_values.append(x)

    sorted_values = sorted(set(delta_x_values))  # Remove duplicates and sort
    delta_x_min = sorted_values[0]  # Smallest value
    xi_list = []
    ti_list = []
    delta_xi_list = []

    for j in range(int(len(LT_x)*0.50), int(len(LT_x)*0.75)):
        if (LT_x[j+1] - LT_x[j])/0.010 < (delta_x_min/beta):
            xi_list.append(LT_x[j])
            ti_list.append(LT_time[j])
            delta_xi_list.append(abs(LT_x[j+1] - LT_x[j])/0.010)
            if (LT_x[j+2] - LT_x[j+1])/0.010 >= (delta_x_min/beta):
                break

    k = len(ti_list) - 1
    index_delta_xi_min = delta_xi_list.index(min(delta_xi_list, key=abs))
    xi = xi_list[index_delta_xi_min]
    ti = ti_list[index_delta_xi_min]
    t_width = (ti_list[k] - ti_list[0])/3 # The time seems to be off by a factor of 3 in the data?

    # Plot the data
    # plt.figure(figsize=(8, 5))
    # plt.plot(xi_list, delta_xi_list, label="LT_x vs LT_time", color="blue")
    # Mark the detected tape cut point
    # plt.scatter(xi, ti, color="red", label=f"Tape Cut at (t={ti:.2f}, x={xi:.2f})", zorder=3)
    # Labels and legend
    # plt.xlabel("Time [s]")
    # plt.ylabel("X Position [mm]")
    # plt.title("X vs Time with Tape Cut Detection")
    # plt.legend()
    # plt.grid(True)
    # plt.show()

    return xi, t_width

def LLS_sync(tow:int, sensor_type:str, overwrite=False):
    width_velocities = [] # Set up list of velocities
    widths = Handling_ALL_Functions.get_processed_data(tow, sensor_type, overwrite)["width"] #gets just the width-column
    times = Handling_ALL_Functions.get_processed_data(tow, sensor_type, overwrite)["time"] #gets just the time-column


    for i in range(len(widths)-1):
        width_velocities.append(widths[i+1] - widths[i])
    width_velocities.append(width_velocities[-1]) # dirty trick to match lengths

    xi, t_width = find_x930(Handling_ALL_Functions.get_processed_data(tow, "LT")["x"], Handling_ALL_Functions.get_processed_data(tow, "LT")["time"])
    if sensor_type == "LLS_B":
        t_width = 2*t_width
        start_time = 4
        end_time = 5.5
    if sensor_type == "LLS_A":
        t_width = 1.5*t_width
        start_time = 4
        end_time = 5.5
    index_stop, time_stop = scan_for_min(t_width, times, width_velocities, start_time, end_time)    

    ##########################################################################################################

    # #Loop over all the data points and store results
    # for i in range(len(widths)-1): 
    #     width_velocity = (widths[i+1] - widths[i]) / (times[i+1] - times[i])
    #     width_velocities.append(width_velocity)

    # plt.plot(times, width_velocities, label="width_velocities", color="red")
    # plt.title("Width velocity")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Rate of change of tow width [m/s]")
    # plt.plot(time_stop,0, "-o")
    # plt.grid()
    # plt.show() 
    return time_stop


def scan_for_min(t_len: float, times: list, values: list, start_time: float, end_time: float) -> tuple:
    """Finds the minimum squared sum over a given time window.
    
    Returns the index and time where the minimum starts.
    Handles negative values by taking absolute differences.
    Only considers values between start_time and end_time.
    """
    
    # Check if the given time range is valid
    if end_time - start_time < t_len:
        raise ValueError(f"Start and end times too close: {end_time - start_time:.2f}, required: {t_len:.2f}")
    
    # Find the index where the start_time begins
    ti = 0
    while ti < len(times) and times[ti] < start_time:
        ti += 1

    sums = []
    min_sum = float('inf')
    min_index = -1

    for i in range(ti, len(values)):
        if times[i] + t_len > end_time:
            break  # Ensure we stay within the time range

        sum_x = 0
        j = i
        while j < len(values) and times[j] <= times[i] + t_len:
            sum_x += values[j] ** 2
            j += 1

        sums.append(sum_x)

        # Keep track of the minimum sum
        if sum_x < min_sum:
            min_sum = sum_x
            min_index = i  # Store the absolute index in `times`

    if min_index == -1:
        raise ValueError("No valid range found within the specified time window.")

    return min_index, times[min_index]

def camera_sync(tow:int, overwrite=False):
    """This function grabs a sample of the CAM data where we know the tape is being layed down
        and then calculates the distance between consective data points. Once the minimum
        distance between data points has been found in the sample, then for data points after
        the sample, if the distance between them is smaller than some factor beta times the minimum
        distance found in the sample, then we know that the tape has been cut and xi = 930mm.
        Then the coressponding time at xi is ti and this time can be used to sync the CAM data with
        other data sets"""

    center_velocities = [] # Set up list of velocities
    centers = Handling_ALL_Functions.get_processed_data(tow, "CAM", overwrite)["center"] #gets just the width-column
    times = Handling_ALL_Functions.get_processed_data(tow, "CAM", overwrite)["time"] #gets just the time-column


    for i in range(len(centers)-1):
        center_velocities.append(centers[i+1] - centers[i])
    center_velocities.append(center_velocities[-1]) # dirty trick to match lengths

    xi, t_width = find_x930(Handling_ALL_Functions.get_processed_data(tow, "LT")["x"], Handling_ALL_Functions.get_processed_data(tow, "LT")["time"])
    t_width = 1.5*t_width
    start_time = 4.5
    end_time = 5.75
    index_stop, time_stop = scan_for_min(t_width, times, center_velocities, start_time, end_time)    

    ##########################################################################################################



    # #Loop over all the data points and store results
    # for i in range(len(widths)-1): 
    #     width_velocity = (widths[i+1] - widths[i]) / (times[i+1] - times[i])
    #     width_velocities.append(width_velocity)

    # plt.plot(times, center_velocities, label="center_velocities", color="red")
    # plt.title("center velocity")
    # plt.xlabel("Time [s]")
    # plt.ylabel("Rate of change of tow center [m/s]")
    # plt.plot(time_stop,0, "-o")
    # plt.grid()
    # plt.show() 

    return time_stop

def least_squares_regression(x, y):
    """
    Performs least squares regression on two lists of error values.
    
    Parameters:
    x (list of float): Independent variable.
    y (list of float): Dependent variable.
    
    Returns:
    tuple: (slope, intercept) of the regression line.
    """
    x = np.array(x)
    y = np.array(y)
    A = np.vstack([x, np.ones(len(x))]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    return slope, intercept

def plot_errors(error1, error2, error3, error4, error5, error6):
    """
    Takes in 6 lists and generates a single plot with subplots for each combination of error types,
    including least squares regression lines.
    
    Parameters:
    error1, error2, error3, error4, error5, error6 (list of float): Lists of error values.
    """
    errors = [error1, error2, error3, error4, error5, error6]
    
    if any(len(errors[0]) != len(err) for err in errors):
        raise ValueError("All error lists must have the same length.")
    
    combinations = list(itertools.combinations(range(6), 2))
    num_plots = len(combinations)
    cols = 3
    rows = (num_plots + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (i, j) in enumerate(combinations):
        x = errors[i]
        y = errors[j]
        slope, intercept = least_squares_regression(x, y)
        
        axes[idx].scatter(x, y, color='b', alpha=0.7, edgecolors='k', label="Data")
        axes[idx].set_xlabel(f"Error {i+1}")
        axes[idx].set_ylabel(f"Error {j+1}")
        axes[idx].set_title(f"Error {i+1} vs Error {j+1}")
        
        # Plot regression line
        x_vals = np.linspace(min(x), max(x), 100)
        y_vals = slope * x_vals + intercept
        axes[idx].plot(x_vals, y_vals, color='r', linestyle='--', label="Regression Line")
        
        axes[idx].grid(True, linestyle='--', alpha=0.6)
        axes[idx].legend()
    
    for idx in range(num_plots, len(axes)):
        fig.delaxes(axes[idx])
    
    plt.tight_layout()
    plt.show()

def plot_two_columns(dataframe1:pd.DataFrame, dataframe2:pd.DataFrame, column1:str, column2:str):
    """plots two columns against time compared to each other, Normalized"""



    data1= dataframe1[column1]
    data2 = dataframe2[column2]
    data1 = (data1-data1.mean())/data1.std()
    data2 = (data2-data2.mean())/data2.std()

    plt.plot(dataframe1["time"], data1, label = column1)
    plt.plot(dataframe2["time"], data2, label = column2)
    plt.xlabel("Time")
    plt.ylabel("Data (Normalized)")
    plt.legend()
    plt.show()

def _get_synced_data(tow:int, *args:str, overwrite:bool = False)->pd.DataFrame:
    '''gets the synced data of the given tow, input is a variable number of datatype keys\n
    valid keys are "LT","LLS_A","LLS_B","CAM"'''
    
    # checks that inputs are valid:
    for sensor_type in args:
        if sensor_type not in ["LT","LLS_A","LLS_B","CAM"]:
            raise KeyError(f"the Key {sensor_type} was invalid: No such data exists")
    if tow not in range(1,32):
        raise IndexError(f"Tow ID {tow} is out of range")

    # get the list of dataframes:
    frame_list = []
    for arg in args:
        frame = Handling_ALL_Functions.get_processed_data(tow,arg,overwrite)
        frame_list.append(arg, frame) # adding both the key (arg) and the frame so we know which frame is which
    
    #TODO: put all the syncing functions here to get the data synced...

    # find time discrepancy
    true_time = blue_dot_LT(tow,overwrite)
    blue_dot_CAM = camera_sync(tow,overwrite)
    blue_dot_LLS_A = LLS_sync(tow, "LLS_A", overwrite)
    blue_dot_LLS_B = LLS_sync(tow, "LLS_B", overwrite)


    # join data in time

    # shift position

    # export

    raise NotImplementedError
    return ...

def main():
    for k in range(1,32):
        _get_synced_data(k, "LT","LLS_A","LLS_B","CAM")

if __name__ == "__main__":
    main()
