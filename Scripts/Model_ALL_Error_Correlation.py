

import Handling_ALL_Functions
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools

def join_data(frame1:pd.DataFrame, frame2:pd.DataFrame, shift)-> pd.DataFrame:
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

<<<<<<< Updated upstream
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



def find_x930(LT_x: list, LT_time):
=======
def find_x930(LT_x: list, LT_time: list):
>>>>>>> Stashed changes
    """This function grabs a sample of the LT data where we know the tape is being layed down
        and then calculates the distance between consective data points. Once the minimum
        distance between data points has been found in the sample, then for data points after
        the sample, if the distance between them is smaller than some factor beta times the minimum
        distance found in the sample, then we know that the tape has been cut and xi = 930mm.
        Then the coressponding time at xi is ti and this time can be used to sync the LT data with
        other data sets"""

    beta = 1/5000
    delta_x_values = []

    for i in range(600,1300):
        delta_x = abs(LT_x[i+1] - LT_x[i])
        delta_x_values.append(delta_x)

        sorted_values = sorted(set(delta_x_values))  # Remove duplicates and sort
        if sorted_values[0] != 0:
            delta_x_min = sorted_values[0]  # Second smallest value
        elif sorted_values[0] == 0:
            delta_x_min = sorted_values[1]  # Second smallest value
        else:
            delta_x_min = None  # No second minimum available
    
    print(delta_x_min)
    xi_list = []
    ti_list = []

    for j in range(1300,len(LT_x)-2):
        if abs(LT_x[j+1] - LT_x[j]) < (delta_x_min/beta):
            xi_list.append(LT_x[j])
            ti_list.append(LT_time[j])
            if abs(LT_x[j+2] - LT_x[j+1]) >= (delta_x_min/beta):
                xi = xi_list[0]
                ti = ti_list[0]
                xn = LT_x[j+1]
                tn = LT_time[j+1]
                t = tn - ti
                break
        
    return xi, t

def LLS_sync(tow:int, sensor_type:str, overwrite=False):
    width_velocities = [] # Set up list of velocities
    delta_width_list = []
    data = Handling_ALL_Functions.get_processed_data(tow, sensor_type, overwrite) # get data, first argument 1-31, second has to stay "LLS_B"
    widths = data.iloc[:,1].values #gets just the width-column
    times = data.iloc[:,0].values #gets just the time-column
    beta = 2.5

    for i in range(len(widths)-1):
        width_velocities.append(widths[i+1] - widths[i])
    width_velocities.append(width_velocities[-1]) # dirty trick to match lengths

    ###########################################################################################################

    for i in range(200,300):
        delta_width = abs(widths[i+1] - widths[i])
        delta_width_list.append(delta_width)
    
        sorted_values = sorted(set(delta_width_list))  # Remove duplicates and sort

        if len(sorted_values) > 1:
            second_min = sorted_values[1]  # Second smallest value
        else:
            second_min = None  # No second minimum available

    print("Second Minimum:", second_min)

    delta_width_min = second_min
    
    xi, t = find_x930(Handling_ALL_Functions.get_processed_data(1, "LT")["x"], Handling_ALL_Functions.get_processed_data(1, "LT")["time"])
    index_stop, time_stop = scan_for_min(t, times, width_velocities)    
    

    print(time_stop)
    ##########################################################################################################



    # #Loop over all the data points and store results
    # for i in range(len(widths)-1): 
    #     width_velocity = (widths[i+1] - widths[i]) / (times[i+1] - times[i])
    #     width_velocities.append(width_velocity)

    plt.plot(times, width_velocities, label="width_velocities", color="red")
    plt.title("Width velocity")
    plt.xlabel("Time [s]")
    plt.ylabel("Rate of change of tow width [m/s]")
    plt.plot(time_stop,0, "-o")
    plt.grid()
    plt.show() 

def scan_for_min(t_len:float, times:list, values:list)->tuple:
    '''finds the minimum range for the given length and returns the index and time where the minimum starts\n
    also makes the diffference absolute to cope with negative values'''

    sums = []
    try:
        for i in range(len(values)):
            sum_x = 0
            j = i
            
            while times[j] <= times[i] + t_len:
                sum_x += values[j]**2
                j+=1
            sums.append(sum_x)
    except IndexError:
        pass # now we're at the end so no point going further

    minimum = min(sums)
    min_index = sums.index(minimum)

    return min_index, times[min_index]

def camera_sync(cam_data: list, cam_time: list):
    """This function grabs a sample of the CAM data where we know the tape is being layed down
        and then calculates the distance between consective data points. Once the minimum
        distance between data points has been found in the sample, then for data points after
        the sample, if the distance between them is smaller than some factor beta times the minimum
        distance found in the sample, then we know that the tape has been cut and xi = 930mm.
        Then the coressponding time at xi is ti and this time can be used to sync the CAM data with
        other data sets"""

    beta = 2
    delta_center_values = []

    for i in range(100,200):
        delta_center = abs(cam_data[i+1] - cam_data[i])
        delta_center_values.append(delta_center)
    
    delta_center_min = min(delta_center_values)

    for j in range(200,len(cam_data)):
        if abs(cam_data[j+1] - cam_data[j]) < (delta_center_min/beta):
            ci = cam_data[j]
            ti = cam_time[j]
            break
        
    return ci, ti

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

    for k in range(1, 32):
        LLS_sync(k, "LLS_B")




def main():
    pass
   



if __name__ == "__main__":
    main()
