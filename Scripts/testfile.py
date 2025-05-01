import pandas as pd
import matplotlib.pyplot as plt
from Handling_ALL_Functions import get_synced_data
from constants import tow_width_specified, y_increment_programmed

def tow_visualizer(tows: list[pd.DataFrame], y_intended: list, name: str, ideal: bool):
    """
    This function takes a list of dataframes that contains features of a tows and plots the corresponding tows in one figure, as well as the ideal tow. 
    The data it takes from that dataframe are
    the centerline, width and x-position. It is important that the columns in the dataframe are properly named.
    For this, check that the centerline column is named "center_CAM", the width after compaction column is named
    "width_LLS_B" and the x-position columns is called "x".
    Arguments are:
    tows: list[pd.DataFrame], the dataframes of the tows
    y_intended: list, list of programmed centerline y-values of the tows
    name: str, the name of the operation that was done to obtain the dataframes of the tows, will be the title of the graph.
    ideal: bool, plots one ideal tow if true
    
    Author: Martijn
    """
    # Check if all elements are DataFrames
    if not all(isinstance(tow, pd.DataFrame) for tow in tows):
        raise TypeError("All elements in 'tows' must be pandas DataFrames.")
    
    #set figure size
    #plt.figure(figsize=(15, 2))
    
    for i in range(len(y_intended)):
        CAM_centerline = tows[i]["center_CAM"] #take the centerline from CAM
        LT_y = tows[i]["y"] #take the y-position from LT
        intended_centerline = y_intended[i] #take the programmed y-value for a straight line
        centerline = CAM_centerline + LT_y + intended_centerline #calculate centerline in space by combining datatypes
        width = tows[i]["width_LLS_B"] #take the width from LLS B
        x = tows[i]["x"]  #take the x-position from LT
        
        
        #make the plots
        if i == 0:
            plt.plot(x, centerline, label="actual centerline", linestyle='dashed', color='grey') #plots the centerline
            plt.plot(x, centerline + 0.5 * width, label="actual tow", linestyle='solid', color='black') #plots the top edge
            plt.plot(x, centerline - 0.5 * width, linestyle='solid', color='black') #plots the bottom edge
        
        else: #do not assign a label to all other tows as this makes the legend unreadable
            plt.plot(x, centerline, linestyle='dashed', color='grey') #plots the centerline
            plt.plot(x, centerline + 0.5 * width, linestyle='solid', color='black') #plots the top edge
            plt.plot(x, centerline - 0.5 * width, linestyle='solid', color='black') #plots the bottom edge

        #plots the start end endlines of the tow
        plt.plot([x.iloc[0], x.iloc[0]], [centerline.iloc[0] - 0.5 * width.iloc[0], centerline.iloc[0] + 0.5 * width.iloc[0]], linestyle='solid', color='black')
        plt.plot([x.iloc[-1], x.iloc[-1]], [centerline.iloc[-1] - 0.5 * width.iloc[-1], centerline.iloc[-1] + 0.5 * width.iloc[-1]],linestyle='solid', color='black')
    
    if ideal == True:
        #plot the ideal tow (just a rectangle)
        plt.plot([0,1000], [tow_width_specified * 0.5, tow_width_specified * 0.5], color='green', label='ideal tow')
        plt.plot([0,1000], [-tow_width_specified * 0.5, -tow_width_specified * 0.5], color='green')
        plt.plot([0,0], [tow_width_specified * 0.5, -tow_width_specified * 0.5], color='green')
        plt.plot([1000,1000], [tow_width_specified * 0.5, -tow_width_specified * 0.5], color='green')
        plt.plot([0,1000], [0,0], color='green', linestyle='dashed', label='ideal centerline')


    # calculate the dimensions of the plots
    x_min = min(min(tow["x"].min() for tow in tows) - 50, -50)
    x_max = max(max(tow["x"].max() for tow in tows) + 50, 1050)
    y_min = min(min(tow["y"].min() for tow in tows) - 100, -50)
    y_max = max(max(tow["y"].max() for tow in tows) + 50, 1050)
    
    #plot info
    plt.xlabel("x-position [mm]")
    plt.ylabel("y-position [mm]")
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid()
    plt.title(name)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.show()

tows = []
y_intended = []

for i in range(1,32):
    tow = get_synced_data(i)
    tows.append(tow)
    y_tow = 125 + (i-1) * y_increment_programmed
    y_intended.append(y_tow)

tow_visualizer(tows, y_intended, "test with all tows", ideal=True)