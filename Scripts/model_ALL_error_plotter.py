import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import Handling_ALL_Functions as hf
from Handling_ALL_Functions import get_processed_data

#TODO: Change all functions. It is only possible to plot one graph per function call
#TODO: Make each function only to plot one error vs time/distance
#TODO: We need to call the function four times for the four error types.


# Plot the error of each sensor vs. Distance
'''Note: It might be necessary to change the names of the errors when calling the DataFrame 'data'.
    For example: In the below function, I call data['error_LLS_A'],
    but the name in the DataFrame might not be the same!,
    so it may be necessary to change it either in all functions 
    or in the DataFrame where the data is stored!'''
def error_vs_distance_plot(df_lls_a, df_lls_b, df_lt, df_cam, title: str):
    # Create a 2x2 grid (ax) for subplots
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))  
    fig.suptitle(title)  # Set main title for the figure

    '''I created a for loop to plot the errors of the four sensors vs. distance,
        so that I don't have to write so much code.
        Each sensor uses its OWN distance axis now, so no one is cut short.
        Written by: Manuel Cruz'''

    # Plot the error of each sensor vs. distance

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT     = Laser tracker 
        error_CAM    = Camera '''

    # I created two lists for distance and error, to easily loop over the four sensors
    errors = [
        df_lls_a['error_LLS_A'], 
        df_lls_b['error_LLS_B'], 
        df_lt['error_LT'], 
        df_cam['center']
    ]
    distances = [
        df_lls_a['distance'], 
        df_lls_b['distance'], 
        df_lt['distance'], 
        df_cam['distance']
    ]
    
    # Descriptive subplot titles
    titles = ['Error LLS A vs. distance', 
              'Error LLS B vs. distance',
              'Error Laser Tracker vs. distance',
              'Error Camera vs. distance']

    # Loop over all sensors to generate each subplot
    for i in range(4):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        # Just plotting and creating titles and labels for the plots
        ax[row, col].plot(distances[i], errors[i])
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel('Distance')
        ax[row, col].set_ylabel('Error')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()



# Plot the error of each sensor vs. time
'''Note: It might be necessary to change the names of the errors when calling the DataFrame 'data'.
    For example: In the below function, I call data['error_LLS_A'],
    but the name in the DataFrame might not be the same!,
    so it may be necessary to change it either in all functions 
    or in the DataFrame where the data is stored!'''

def error_vs_time_plot(df_lls_a, df_lls_b, df_lt, df_cam, title: str):
    # Create a 2x2 grid (ax) for subplots
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))  
    fig.suptitle(title)  # Set main title for the figure

    '''I created a for loop to plot the errors of the four sensors vs. time,
        so that I don't have to write so much code.
        Each sensor uses its OWN time axis now, so no one is cut short.
        Written by: Manuel Cruz'''

    # Plot the error of each sensor vs. time
    
    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT     = Laser tracker 
        error_CAM    = Camera '''

    # I created two lists for time and error, to easily loop over the four sensors
    errors = [
        df_lls_a['error_LLS_A'], 
        df_lls_b['error_LLS_B'], 
        df_lt['error_LT'], 
        df_cam['error_CAM']
    ]
    times = [
        df_lls_a['time'], 
        df_lls_b['time'], 
        df_lt['time'], 
        df_cam['time']
    ]
    
    # Descriptive subplot titles
    titles = ['Error LLS A vs. time', 
              'Error LLS B vs. time',
              'Error Laser Tracker vs. time',
              'Error Camera vs. time']

    # Loop over all sensors to generate each subplot
    for i in range(4):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        # Just plotting and creating titles and labels for the plots
        ax[row, col].plot(times[i], errors[i])
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel('Time (s)')
        ax[row, col].set_ylabel('Error')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()


# Plot every error line in the same plot vs. X distance
'''Note: It might be necessary to change the names of the errors when calling the DataFrame 'data'.
    For example: In the below function, I call data['error_LLS_A'],
    but the name in the DataFrame might not be the same!,
    so it may be necessary to change it either in all functions 
    or in the DataFrame where the data is stored!'''
def all_errors_vs_distance_plot(data: pd.DataFrame, title:str):

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title('All errors vs. distance')  # Set main title for the figure
    ax.set_xlabel('Distance')
    ax.set_ylabel('Error')

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_CAM = camera '''

    ax.plot(data['distance'], data['error_LLS_A'])
    ax.plot(data['distance'], data['error_LLS_B'])
    ax.plot(data['distance'], data['error_LT'])
    ax.plot(data['distance'], data['error_CAM'])

    # Identify every line in the plot
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Plot every error line in the same plot vs. time
    '''Note: It might be necessary to change either the names of the errors when calling data.
    For example: in data['error_LLS_A'] the name in the dataframe might not be the same,
    so it may be necessary to change it!'''
def all_errors_vs_time_plot(data: pd.DataFrame, title:str):

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title('All errors vs. time')  # Set main title for the figure
    ax.set_xlabel('time')
    ax.set_ylabel('Error')

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_CAM = camera '''

    ax.plot(data['time'], data['error_LLS_A'])
    ax.plot(data['time'], data['error_LLS_B'])
    ax.plot(data['time'], data['error_LT'])
    ax.plot(data['time'], data['center'])

    # Identify every line in the plot
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()


# Change the tow number to get the data for the desired tow
tow = 10

# Load and rename error columns as needed
df_lls_a = get_processed_data(tow, 'LLS_A').rename(columns={'width error': 'error_LLS_A'})
df_lls_b = get_processed_data(tow, 'LLS_B').rename(columns={'width error': 'error_LLS_B'})
df_lt    = get_processed_data(tow, 'LT')
df_cam   = get_processed_data(tow, 'CAM')



# Now call the function
error_vs_time_plot(df_lls_a, df_lls_b, df_lt, df_cam, title=f"Errors vs Time for Tow {tow}")



'''There is still no data for the distance column in the dataframes, so the function will not work.'''
#TODO: Add the distance column to the dataframes to make the function work.
# error_vs_distance_plot(df_lls_a, df_lls_b, df_lt, df_cam, title=f"Errors vs Distance for Tow {tow}")



# This is just a backup algorithm (hard-coded) in case the for loop doesn't work.
'''def error_vs_distance_plot(data: pd.DataFrame, title: str):
    # Plot the error of each sensor vs. distance

    error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_CAM = camera
    
    error_LLS_A = data['error_LLS_A']
    error_LLS_B = data['error_LLS_B']
    error_LT = data['error_LT']
    error_CAM = data['error_CAM']

    fig, ax = plt.subplots()

    # Plot the error of LLS A vs distance
    ax[0, 0].plot(data['distance'], error_LLS_A)
    ax[0, 0].set_title('Error LLS A vs. distance')
    ax[0, 0].set_xlabel('X Position')
    ax[0, 0].set_ylabel('Error LLS A')

    # Plot the error of LLS B vs. distance 
    ax[0, 1].plot(data['distance'], error_LLS_B)
    ax[0, 1].set_title('Error LLS B vs. distance')
    ax[0, 1].set_xlabel('X Position')
    ax[0, 1].set_ylabel('Error LLS B')

    # Plot the error of Laser Tracker (LT) vs. distance
    ax[1, 0].plot(data['distance'], error_LT)
    ax[1, 0].set_title('Error Laser Tracker vs. distance')
    ax[1, 0].set_xlabel('X Position')
    ax[1, 0].set_ylabel('Error Laser Tracker')

    # Plot the error of camera vs. distance
    ax[1, 1].plot(data['distance'], error_CAM)
    ax[1, 1].set_title('Error camera vs. distance')
    ax[1, 1].set_xlabel('X Position')
    ax[1, 1].set_ylabel('Error camera')

    for i, error in enumerate(errors):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        ax[row, col].plot(data['time'], error)
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel('time')
        ax[row, col].set_ylabel(errors_names[i])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show() '''
    

