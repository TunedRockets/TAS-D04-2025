import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

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