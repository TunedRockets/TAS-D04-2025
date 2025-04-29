'''This is meant to run a large number of simulations at a time.'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from constants import tow_width_specified

from Handling_ALL_Functions import get_synced_data
#from Model_LT_TheoChangeName import generate_error_path as get_LT_dist
#from Model_CAM_ import generate_error_path as get_CAM_dist
#from Model_LLSA import generate_error_path as get_LLSA_dist
#from Model_LLSB import generate_error_path as get_LLSB_dist

from Model_LT_TheoChangeName import generate_error_path as get_LT_path
from Model_CAM_ import generate_error_path as get_CAM_path
from Model_LLSA import generate_error_path as get_LLSA_path
from Model_LLSB import generate_error_path as get_LLSB_path


###### just testing some stuff
from Handling_ALL_Functions import get_synced_data

data = get_synced_data(5)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(data)

def save_distribution_data():
    def export_data(data_table: pd.DataFrame, short_name):
        '''This function saves a pandas dataframe as
            a .pkl, it will be saved with the short name,
            use that to access it'''

        _save_path = "Script\\"

        data_table.to_pickle(_save_path + short_name + ".pkl")
        # note! this does not save headers or indexes. might need to change that depending on how we do
        return

def save_all_distribution_data(_save_path, LT_short_name, CAM_short_name, LLSA_short_name, LLSB_short_name):
    '''This function saves all the data of the distributions generated of the consecutive data.'''
    LT_dist =
    CAM_dist =
    LLSA_dist =
    LLSB_dist =

    LT_dist.columns = ["LT_mean", "LT_std"]
    #LT_dist.columns = ["LT_mean", "LT_std"]
    #LT_dist.columns = ["LT_mean", "LT_std"]
    #LT_dist.columns = ["LT_mean", "LT_std"]

    save_distribution_data(data, LT_short_name)
    save_distribution_data(data, CAM_short_name)
    save_distribution_data(data, LLSA_short_name)
    save_distribution_data(data, LLSB_short_name)





def run_model(dx, save_data: bool=False, use_saved: bool=False):
    if use_saved:
        _save_path = "Script\\"
        LT_short_name = 'LT_Dist_Data'
        CAM_short_name = 'CAM_Dist_Data'
        LLSA_short_name = 'LLSA_Dist_Data'
        LLSB_short_name = 'LLSB_Dist_Data'

        if save_data:
            save_distribution_data(_save_path, LT_short_name, CAM_short_name, LLSA_short_name, LLSB_short_name)
        LT_dist = pd.read_pickle(_save_path + LT_short_name + ".pkl")
        CAM_dist = pd.read_pickle(_save_path + CAM_short_name + ".pkl")
        LLSA_dist = pd.read_pickle(_save_path + LLSA_short_name + ".pkl")
        LLSB_dist = pd.read_pickle(_save_path + LLSB_short_name + ".pkl")

    LT_error_list = get_LT_path()
    CAM_error_list = get_CAM_path()
    LLSA_error_list = get_LLSA_path()
    LLSB_error_list = get_LLSB_path()

    generated_data = []
    x = 0
    for i in range(len(LT_error_list)):
        centerline_error = LT_error_list[i] + CAM_error_list[i]
        width_error = LLSB_error_list[i]
        x +=dx
        generated_data.append([x, centerline_error, width_error])

    generated_data = pd.DataFrame(generated_data, columns = ['x', 'error'])




data = run_model()

def tow_visualizer(tow: pd.DataFrame, name: str):
    """
    This function takes a dataframe that contains features of a tow and plots the corresponding tow, as well as the intended tow. 
    The data it takes from that dataframe are
    the centerline, width and x-position. It is important that the columns in the dataframe are properly named.
    For this, check that the centerline column is named "center_CAM", the width after compaction column is named
    "width_LLS_B" and the x-position columns is called "x".
    Arguments are:
    tow: pd.DataFrame, the dataframe of the tow 
    name: str, the name of the tow, will be the title of the graph.
    
    Author: Martijn
    """
    #Gets the important data, names called in the dataframe might need to be changed depending on what names are 
    #in the final synchronized dataframe
    centerline = tow["center_CAM"]   #take the centerline from CAM
    width = tow["width_LLS_B"]        #take the width from LLS B
    x = tow["x"]                  #take the x-position from LT
    
    #set figure size
    plt.figure(figsize=(15, 2))
    
    #make the plot
    plt.plot(x, centerline, label="actual centerline", linestyle='dashed', color='grey') #plots the centerline
    plt.plot(x, centerline + 0.5 * width, label="actual tow edge", linestyle='solid', color='black') #plots the top edge
    plt.plot(x, centerline - 0.5 * width, linestyle='solid', color='black') #plots the bottom edge

    #plots the start end endlines of the tow
    plt.plot([tow['x'].iloc[0], tow['x'].iloc[0]], [tow['center_CAM'].iloc[0] - 0.5 * tow['width_LLS_B'].iloc[0], tow['center_CAM'].iloc[0] + 0.5 * tow['width_LLS_B'].iloc[0]], linestyle='solid', color='black')
    plt.plot([tow['x'].iloc[-1], tow['x'].iloc[-1]], [tow['center_CAM'].iloc[-1] - 0.5 * tow['width_LLS_B'].iloc[-1], tow['center_CAM'].iloc[-1] + 0.5 * tow['width_LLS_B'].iloc[-1]], linestyle='solid', color='black')

    #plot the programmed path (just a rectangle)
    plt.plot([0,1000], [tow_width_specified * 0.5, tow_width_specified * 0.5], color='green', label='programmed tow edge')
    plt.plot([0,1000], [-tow_width_specified * 0.5, -tow_width_specified * 0.5], color='green')
    plt.plot([0,0], [tow_width_specified * 0.5, -tow_width_specified * 0.5], color='green')
    plt.plot([1000,1000], [tow_width_specified * 0.5, -tow_width_specified * 0.5], color='green')
    plt.plot([0,1000], [0,0], color='green', linestyle='dashed', label='programmed centerline')

    #plot info
    plt.xlabel("x-position [mm]")
    plt.ylabel("y-position [mm]")
    plt.xlim(-50, 1050)
    plt.ylim(-7, 7)
    plt.grid()
    plt.title(name)
    plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    plt.tight_layout()
    plt.show()