# This file is intended to contain a function that plots the edges of a tow.
# This could be any tow, whether it is from experimental data or artificial tows that are generated with the model.
# It will, amongst other uses, allow us to:
    # Check if the syncing was successful
    # Check if the model produces realistic tows
#Author: Martijn

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
    
    #set figure size
    plt.figure(figsize=(15, 2))
    
    #make the plot
    plt.plot(x, centerline, label="centerline", linestyle='dashed', color='grey') #plots the centerline
    plt.plot(x, centerline + 0.5 * width, label="actual tow edge", linestyle='solid', color='black') #plots the top edge
    plt.plot(x, centerline - 0.5 * width, linestyle='solid', color='black') #plots the bottom edge

    #plots the start end endlines of the tow
    plt.plot([tow['x'].iloc[0], tow['x'].iloc[0]], [tow['center_CAM'].iloc[0] - 0.5 * tow['width_LLS_B'].iloc[0], tow['center_CAM'].iloc[0] + 0.5 * tow['width_LLS_B'].iloc[0]], linestyle='solid', color='black')
    plt.plot([tow['x'].iloc[-1], tow['x'].iloc[-1]], [tow['center_CAM'].iloc[-1] - 0.5 * tow['width_LLS_B'].iloc[-1], tow['center_CAM'].iloc[-1] + 0.5 * tow['width_LLS_B'].iloc[-1]], linestyle='solid', color='black')

    #plot the programmed path (just a rectangle)
    plt.plot([0,1000], [tow_width_specified * 0.5, tow_width_specified * 0.5], 'g', label='programmed tow edge')
    plt.plot([0,1000], [-tow_width_specified * 0.5, -tow_width_specified * 0.5], 'g')
    plt.plot([0,0], [tow_width_specified * 0.5, -tow_width_specified * 0.5], 'g')
    plt.plot([1000,1000], [tow_width_specified * 0.5, -tow_width_specified * 0.5], 'g')

    #plot info
    plt.xlabel("x-position [mm]")
    plt.ylabel("y-position [mm]")
    plt.xlim(-50, 1050)
    plt.ylim(-7, 7)
    plt.title(name)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.show()

def main():
    townumber = 3
    tow = get_synced_data(townumber)
    print(tow)
    tow_plotter(tow, f'Tow number {townumber}')

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else