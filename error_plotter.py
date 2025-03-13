import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_error(data: pd.DataFrame, title: str):
    """
    Plots the error of the data
    """
    # Create a figure and a set of subplots
    fig, ax = plt.subplots(2, 2)
    ax.plot(data["time"], data["error"])
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Error")
    plt.show()


def error_vs_distance_plot(data: pd.DataFrame, title: str):
    # Plot the error of each sensor vs. distance

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera'''
    
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

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()

def error_vs_time_plot(data: pd.DataFrame, title: str):
    # Plot the error of each sensor vs. distance

    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera'''
    
    error_LLS_A = data['error_LLS_A']
    error_LLS_B = data['error_LLS_B']
    error_LT = data['error_LT']
    error_camera = data['error_camera']

    fig, ax = plt.subplots()

    for i in range(4):
        ax[i].plot(data['time'], data[f'error_{i}'])
        ax[i].set_title(f'Error {i} vs. time')
        ax[i].set_xlabel('Time')
        ax[i].set_ylabel(f'Error {i}')


