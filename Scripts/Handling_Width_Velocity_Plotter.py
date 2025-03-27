import Handling_ALL_Functions
import matplotlib.pyplot as plt
import pandas as pd
#import numpy as np

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
    
    index_stop, time_stop = scan_for_min(0.6, times, width_velocities)    
    

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


def main():

    for k in range(1, 32):
        LLS_sync(k, "LLS_A")

if __name__ == "__main__":
    main()