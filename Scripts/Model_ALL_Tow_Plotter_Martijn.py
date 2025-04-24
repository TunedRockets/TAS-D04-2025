# This file is intended to contain a function that plots the edges of a tow.
# This could be any tow, whether it is from experimental data or artificial tows that are generated with the model.
# It will, amongst other uses, allow us to:
    # Check if the syncing was successful
    # Check if the model produces realistic tows

import matplotlib.pyplot as plt
import pandas as pd

def tow_plotter(centerline: pd.DataFrame, width: pd.DataFrame):
    
    # plot the centerline (from CAM data)
    plt.plot()



    # add half of the width to both sides to (from LLS B data)

    # at the start and endpoints, add a vertical line to indicate the start and end of the tow
    return 