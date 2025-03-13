import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Plot the error of each sensor vs. Distance
def error_vs_distance_plot(data: pd.DataFrame, title: str):

    '''I created a for loop to plot the errors of the four sensors vs. time,
        so that I don't have to write so much code.
        Written by: Manuel Cruz'''

    # Plot the error of each sensor vs. X position
    
    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera'''
    
    # Create a 2x2 grid (ax) to subplots
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))  
    fig.suptitle(title)  # Set main title for the figure

    # Created lists for the parameters I need in the for loop, because we cannot say 
    # for e.g. data['error_LLS_A'] in a for loop (it has to have an associated number)
    # and in lists you can refer to strings and so on as a number (the index)! 
    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_camera']]
    errors_names = ['error_LLS_A', 'error_LLS_B', 'error_LT','error_camera']
    titles = ['Error LLS A vs. X position', 
              'Error LLS B vs. X position',
              'Error Laser Tracker vs. X position',
              'Error camera vs. X position']

    # Algorithm to make the code more readable than hard-code every plot (see below)
    for i, error in enumerate(errors):
        row = i // 2  # Determine the row of plotting (0 or 1)
        col = i % 2   # Determine the column of plotting (0 or 1)

        # Just plotting and creating titles and labels for the plots
        ax[row, col].plot(data['distance'], error)
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel('Distance')
        ax[row, col].set_ylabel(errors_names[i])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()



# Plot the error of each sensor vs. TIME
def error_vs_time_plot(data: pd.DataFrame, title: str):

    '''I created a for loop to plot the errors of the four sensors vs. time,
        so that I don't have to write so much code.
        Written by: Manuel Cruz'''

    # Plot the error of each sensor vs. time
    
    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera'''
    
    # Create a 2x2 grid (ax) to subplots
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))  
    fig.suptitle(title)  # Set main title for the figure

    # Created lists for the parameters I need in the for loop, because we cannot say 
    # for e.g. data['error_LLS_A'] in a for loop (it has to have an associated number)
    # and in lists you can refer to strings and so on as a number (the index)!
    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_camera']]
    errors_names = ['error_LLS_A', 'error_LLS_B', 'error_LT','error_camera']
    titles = ['Error LLS A vs. time', 
              'Error LLS B vs. time',
              'Error Laser Tracker vs. time',
              'Error camera vs. time']
    
    # Algorithm to make the code more readable than hard-code every plot (see below)
    for i, error in enumerate(errors):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        # Just plotting and creating titles and labels for the plots
        ax[row, col].plot(data['time'], error)
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel('Time')
        ax[row, col].set_ylabel(errors_names[i])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    #TODO: Find mean and standard deviation of the errors
    #todo: create a function to plot all errors in the same plot 

# Plot every error line in the same plot vs. X distance
def all_errors_vs_distance_plot(data: pd.DataFrame, title:str):

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title('All errors vs. distance')  # Set main title for the figure
    ax.set_xlabel('Distance')
    ax.set_ylabel('Error')

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera '''

    ax.plot(data['distance'], data['error_LLS_A'])
    ax.plot(data['distance'], data['error_LLS_b'])
    ax.plot(data['distance'], data['error_LT'])
    ax.plot(data['distance'], data['error_camera'])

    # Identify every line in the plot
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Plot every error line in the same plot vs. time
def all_errors_vs_time_plot(data: pd.DataFrame, title:str):

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_title('All errors vs. time')  # Set main title for the figure
    ax.set_xlabel('Time')
    ax.set_ylabel('Error')

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera '''

    ax.plot(data['Time'], data['error_LLS_A'])
    ax.plot(data['Time'], data['error_LLS_b'])
    ax.plot(data['Time'], data['error_LT'])
    ax.plot(data['Time'], data['error_camera'])

    # Identify every line in the plot
    ax.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()







# This is just a backup algorithm (hard-coded) in case the for loop doesn't work.
'''def error_vs_distance_plot(data: pd.DataFrame, title: str):
    # Plot the error of each sensor vs. distance

    error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera
    
    error_LLS_A = data['error_LLS_A']
    error_LLS_B = data['error_LLS_B']
    error_LT = data['error_LT']
    error_camera = data['error_camera']

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
    ax[1, 1].plot(data['distance'], error_camera)
    ax[1, 1].set_title('Error camera vs. distance')
    ax[1, 1].set_xlabel('X Position')
    ax[1, 1].set_ylabel('Error camera')

    for i, error in enumerate(errors):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        ax[row, col].plot(data['time'], error)
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel('Time')
        ax[row, col].set_ylabel(errors_names[i])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show() '''
    

