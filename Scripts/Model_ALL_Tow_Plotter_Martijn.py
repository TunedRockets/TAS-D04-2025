# This file is intended to contain a function that plots the edges of a tow.
# This could be any tow, whether it is from experimental data or artificial tows that are generated with the model.
# It will, amongst other uses, allow us to:
    # Check if the syncing was successful
    # Check if the model produces realistic tows

import matplotlib.pyplot as plt
import pandas as pd
from Handling_ALL_Functions import get_synced_data

def tow_plotter(tow: pd.DataFrame, name: str):
    
    #Gets the important data, might need to be changed depending on what names are in the final synchronized dataframe
    centerline = tow["center"]
    width = tow["width"]
    x = tow["x"]
    
    # make the plot
    fig, ax = plt.subplots()
    ax.plot(x, centerline, label="centerline", )
    ax.plot(x, centerline + 0.5 * width, label="top edge")
    ax.plot(x, centerline - 0.5 * width, label="bottom edge")
    ax.vline()
    plt.xlabel("x-position [mm]")
    plt.ylabel("tow outline")
    plt.title(name)
    plt.legend()
    plt.show(fig)


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