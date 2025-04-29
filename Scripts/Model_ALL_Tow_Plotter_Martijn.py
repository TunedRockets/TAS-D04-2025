# This file is intended to contain a function that plots the edges of a tow.
# This could be any tow, whether it is from experimental data or artificial tows that are generated with the model.
# It will, amongst other uses, allow us to:
    # Check if the syncing was successful
    # Check if the model produces realistic tows

import matplotlib.pyplot as plt
import pandas as pd
from Handling_ALL_Functions import get_synced_data
from constants import tow_width_specified

def tow_plotter(tow: pd.DataFrame, name: str):
    
    #Gets the important data, names called in the dataframe might need to be changed depending on what names are 
    #in the final synchronized dataframe
    centerline = tow["center_CAM"]   #take the centerline from CAM
    width = tow["width_LLS_B"]        #take the width from LLS B
    x = tow["x"]                  #take the x-position from LT
    
    # make the plot
    plt.plot(x, centerline, label="centerline", linestyle='dashed') #plots the centerline
    plt.plot(x, centerline + 0.5 * width, label="top edge", linestyle='solid') #plots the top edge
    plt.plot(x, centerline - 0.5 * width, label="bottom edge", linestyle='solid') #plots the bottom edge

    #plots the start end endlines of the tow
    plt.plot([tow['x'].iloc[0], tow['x'].iloc[0]], [tow['center_CAM'].iloc[0] - 0.5 * tow['width_LLS_B'].iloc[0], tow['center_CAM'].iloc[0] + 0.5 * tow['width_LLS_B'].iloc[0]], linestyle='solid', label="starting line")
    plt.plot([tow['x'].iloc[-1], tow['x'].iloc[-1]], [tow['center_CAM'].iloc[-1] - 0.5 * tow['width_LLS_B'].iloc[-1], tow['center_CAM'].iloc[-1] + 0.5 * tow['width_LLS_B'].iloc[-1]], linestyle='solid', label="cut off line")

    #plot the programmed path (just a rectangle)
    plt.plot([0,1000], [tow_width_specified * 0.5, tow_width_specified * 0.5])
    plt.plot([0,1000], [-tow_width_specified * 0.5, -tow_width_specified * 0.5])
    plt.plot([0,0], [tow_width_specified * 0.5, -tow_width_specified * 0.5])
    plt.plot([1000,1000], [tow_width_specified * 0.5, -tow_width_specified * 0.5])

    #plot info
    plt.xlabel("x-position [mm]")
    plt.ylabel("tow outline [mm]")
    plt.title(name)
    plt.legend()
    plt.show()

def main():
    townumber = 3
    tow = get_synced_data(townumber)
    print(tow)
    tow_plotter(tow, f'Tow number {townumber}')

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else