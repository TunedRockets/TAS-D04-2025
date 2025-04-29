# This file is intended to contain a function that plots the edges of a tow.
# This could be any tow, whether it is from experimental data or artificial tows that are generated with the model.
# It will, amongst other uses, allow us to:
    # Check if the syncing was successful
    # Check if the model produces realistic tows

import matplotlib.pyplot as plt
import pandas as pd
from Handling_ALL_Functions import get_synced_data

def tow_plotter(tow: pd.DataFrame, name: str):
    
    #Gets the important data, names called in the dataframe might need to be changed depending on what names are 
    #in the final synchronized dataframe
    centerline = tow["CAMcenter"]   #take the centerline from CAM
    width = tow["LLSBwidth"]        #take the width from LLS B
    x = tow["LTx"]                  #take the x-position from LT
    
    # make the plot
    
    plt.plot(x, centerline, label="centerline", linestyle='k--') #plots the centerline
    plt.plot(x, centerline + 0.5 * width, label="top edge", linestyle='k-') #plots the top edge
    plt.plot(x, centerline - 0.5 * width, label="bottom edge", linestyle='k-') #plots the bottom edge

    #plots the start end endlines of the tow
    plt.plot([x[0], x[0]], [centerline[0] - 0.5 * width[0], centerline[0] + 0.5 * width[0]], linestyle='k-', label="starting line")
    plt.plot([x[-1], x[-1]], [centerline[-1] - 0.5 * width[-1], centerline[-1] + 0.5 * width[-1]], linestyle='k-', label="cut off line")

    plt.xlabel("x-position [mm]")
    plt.ylabel("tow outline")
    plt.title(name)
    plt.legend()
    plt.show()


tow = get_synced_data(1)
print(tow)
tow_plotter(tow, "some name")
""" 
def main():
    # force-recompute LT data for tows 1–31 and print first rows
    for k in range(1, 32):
        df_cam = get_processed_data(k, "LT", overwrite=False)
        print(df_cam.head())


if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else

""" 