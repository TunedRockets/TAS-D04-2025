import Handling_ALL_Functions
import matplotlib.pyplot as plt
#import numpy as np

def Width_Velocity_Plotter(tow:int):
    width_velocities = [] # Set up list of velocities
    delta_width_list = []
    data = Handling_ALL_Functions.get_processed_data(tow, "LLS_B") # get data, first argument 1-31, second has to stay "LLSB"
    widths = data.iloc[:,1].values #gets just the width-column
    times = data.iloc[:,0].values #gets just the time-column
    beta = 1.5

###########################################################################################################

    for i in range(200,350):
        delta_width = abs(widths[i+1] - widths[i])
        delta_width_list.append(delta_width)
    
        sorted_values = sorted(set(delta_width_list))  # Remove duplicates and sort

        if len(sorted_values) > 1:
            second_min = sorted_values[1]  # Second smallest value
        else:
            second_min = None  # No second minimum available

    print("Second Minimum:", second_min)

    delta_width_min = second_min
    
    width_stop = None
    time_stop = None
    
    for j in range(350,len(widths)):
        if abs(widths[j] - widths[j-1]) < (delta_width_min/beta):
            width_stop = widths[j-1]
            time_stop = times[j-1]
            break

    
    print(width_stop)
    print(time_stop)
##########################################################################################################



    #Loop over all the data points and store results
    for i in range(len(widths)-1): 
        width_velocity = (widths[i+1] - widths[i]) / (times[i+1] - times[i])
        width_velocities.append(width_velocity)

    plt.plot(times[:-1], width_velocities, label="width_velocities", color="red")
    plt.title("Width velocity")
    plt.xlabel("Time [s]")
    plt.ylabel("Rate of change of tow width [m/s]")
    plt.grid()
    plt.show() 


Width_Velocity_Plotter(10)