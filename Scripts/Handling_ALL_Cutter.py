import math
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

from Model_ALL_Error_Correlation import find_x930
import Handling_ALL_Functions


def LT_time_sync(tow: int, data: pd.DataFrame):
    xi, t_width = find_x930(Handling_ALL_Functions.get_processed_data(tow, "LT")["x"],
                            Handling_ALL_Functions.get_processed_data(tow, "LT")["time"])
    x_0 = xi - 930
    x_end = x_0 + 1000

    t_list = data['time']
    x_list = data['x']
    for i in range(len(x_list)):
        x = x_list[i]
        if x >= x_0:
            t_0 = t_list[i]
            break

    for i in range(len(x_list)):
        x = x_list[i]
        if x >= x_end:
            t_end = t_list[i]
            break

    return t_0, t_end

def LT_cutter(data: pd.DataFrame, t_0: float, t_end: float):
    t_list = data['time']

    for i in range(len(t_list)):
        t = t_list[i]
        if t >= t_0:
            start = i
            break

    for i in range(len(t_list)):
        t = t_list[i]
        if t >= t_end:
            end = i
            break

    rows = (end - start) + 1
    columns = len(data[0])
    shape = (rows, columns)
    pandas_table = np.empty(shape)

    for i in range(start, end+1):
        pandas_table[i][0] = data['time'][i] - t_0
        pandas_table[i][1] = data['x'][i]
        pandas_table[i][2] = data['y'][i]
        pandas_table[i][3] = data['z'][i]
        pandas_table[i][4] = data['error_LT'][i]  # This is the y-error, it is just a better naming
        pandas_table[i][5] = data['z_error'][i]
    # (Optional) Rename the columns to something more readable:
    pandas_table = pd.DataFrame(pandas_table)
    pandas_table.columns = ["time", "x", "y", "z", "error_LT", "z error"]

    return pandas_table

def LLS_cutter(data: pd.DataFrame, t_0: float, t_end: float):
    t_list = data['time']

    for i in range(len(t_list)):
        t = t_list[i]
        if t >= t_0:
            start = i
            break

    for i in range(len(t_list)):
        t = t_list[i]
        if t >= t_end:
            end = i
            break

    rows = (end - start) + 1
    columns = len(data[0])
    shape = (rows, columns)
    pandas_table = np.empty(shape)

    for i in range(start, end + 1):
        pandas_table[i][0] = data['time'][i] - t_0
        pandas_table[i][1] = data['width'][i]
        pandas_table[i][2] = data['center'][i]
        pandas_table[i][3] = data['width error'][i]
    # (Optional) Rename the columns to something more readable:
    pandas_table = pd.DataFrame(pandas_table)
    pandas_table.columns = ["time", "width", "center","width error"]

    return pandas_table


def CAM_cutter(data: pd.DataFrame, t_0: float, t_end: float):
    t_list = data['time']

    for i in range(len(t_list)):
        t = t_list[i]
        if t >= t_0:
            start = i
            break

    for i in range(len(t_list)):
        t = t_list[i]
        if t >= t_end:
            end = i
            break

    rows = (end - start) + 1
    columns = len(data[0])
    shape = (rows, columns)
    pandas_table = np.empty(shape)

    for i in range(start, end + 1):
        pandas_table[i][0] = data['time'][i] - t_0
        pandas_table[i][1] = data['width'][i]
        pandas_table[i][2] = data['center'][i]
        pandas_table[i][3] = data['error_CAM'][i]
    # (Optional) Rename the columns to something more readable:
    pandas_table = pd.DataFrame(pandas_table)
    pandas_table.columns = ["time", "width", "center", "error_CAM"]

    return pandas_table


def import_data(tow: int):
    LT_data = Handling_ALL_Functions.get_processed_data(tow, "LT")
    LLSA_data = Handling_ALL_Functions.get_processed_data(tow, "LLS1")
    LLSB_data = Handling_ALL_Functions.get_processed_data(tow, "LLS2")
    CAM_data = Handling_ALL_Functions.get_processed_data(tow, "CAM")

    return LT_data, LLSA_data, LLSB_data, CAM_data

def export_data(data_table: pd.DataFrame, short_name):
    '''This function saves a pandas dataframe as
        a .pkl, it will be saved with the short name,
        use that to access it'''

    _save_path = "Cut data\\"

    data_table.to_pickle(_save_path + short_name + ".pkl")
    # note! this does not save headers or indexes. might need to change that depending on how we do
    return


def main():
    x_i, t_width = find_x930()

    for n in range(31):
        tow = n+1
        LT_data, LLSA_data, LLSB_data, CAM_data = import_data(tow)

        t_0, t_end = LT_time_sync(tow, LT_data)
        LT_data_cut = LT_cutter(LT_data, t_0, t_end)
        LLSA_data_cut = LLS_cutter(LLSA_data, t_0, t_end)
        LLSB_data_cut = LLS_cutter(LLSB_data, t_0, t_end)
        CAM_data_cut = CAM_cutter(CAM_data, t_0, t_end)

        LT_name = 'LT_' + str(tow)
        LLSA_name = 'LLS_A_' + str(tow)
        LLSB_name = 'LLS_B_' + str(tow)
        CAM_name = 'CAM_' + str(tow)
        print(f'data save names: {LT_name}, {LLSA_name}, {LLSB_name}, {CAM_name}')

        export_data(LT_data_cut, LT_name)
        export_data(LLSA_data_cut, LLSA_name)
        export_data(LLSB_data_cut, LLSB_name)
        export_data(CAM_data_cut, CAM_name)


