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


def error_plotter(data: pd.DataFrame, title: str):
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
    ax.plot(data['distance'], data['error'])
    ax.set_xlabel('X Position')
    ax.set_ylabel('Error')

    plt.show()


