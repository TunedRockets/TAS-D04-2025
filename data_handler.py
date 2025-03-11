"""
for getting data from wherever we save it, and saving the data in that place

not the sorting, importing, or parsing. 

"""

import numpy as np
import pandas as pd

################################################################################################################
"""Functions for Laser Tracker"""

def function(x: list, y: list, z: list, time: list) -> pd.DataFrame:
    rows = len(x)
    columns = 4
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)


    for i in range(len(x)):
        pandas_table[i][0] = (x[i])
        pandas_table[i][1] = (y[i])
        pandas_table[i][2] = (z[i])
        pandas_table[i][3] = (time[i])

    return pandas_table



################################################################################################################
"""Functions for Laser Line Scanner"""




################################################################################################################
"""Functions for Camera"""




################################################################################################################



def main():
    
    # add testing code here
    pass

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else
