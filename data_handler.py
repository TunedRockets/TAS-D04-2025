"""
for getting data from wherever we save it, and saving the data in that place

not the sorting, importing, or parsing. 

"""

import numpy as np
import pandas as pd

################################################################################################################
"""Functions for Laser Tracker"""

def handle_LT(time: list, x: list, y: list, z: list) -> pd.DataFrame:
    rows = len(time)
    columns = 4
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)

    for i in range(len(x)):
        pandas_table[i][0] = (time[i])
        pandas_table[i][1] = (x[i])
        pandas_table[i][2] = (y[i])
        pandas_table[i][3] = (z[i])

    return pandas_table

################################################################################################################
"""Functions for Laser Line Scanner"""

def handle_LLS(time: list, width: list, center: list) -> pd.DataFrame:
    rows = len(time)
    columns = 3
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)

    for i in range(len(time)):
        pandas_table[i][0] = (time[i])
        pandas_table[i][1] = (width[i])
        pandas_table[i][2] = (center[i])

    return pandas_table

################################################################################################################
"""Functions for Camera"""

def handle_camera(time: list) -> pd.DataFrame:
    rows = len(x)
    columns = 1
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)

    for i in range(len(time)):
        pandas_table[i][0] = time[i]

    return pandas_table

################################################################################################################

def main():
    
    # add testing code here
    pass

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else
