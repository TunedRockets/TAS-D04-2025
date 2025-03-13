"""
for getting data from wherever we save it, and saving the data in that place

not the sorting, importing, or parsing. 

"""

import numpy as np
import pandas as pd

################################################################################################################
"""Functions for Laser Tracker"""

def handle_LT(time: list, x: list, y: list, z: list, tow: int) -> pd.DataFrame:
    rows = len(time)
    columns = 5
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)
    error = error_LT(y, z, tow)

    for i in range(len(x)):
        pandas_table[i][0] = time[i]
        pandas_table[i][1] = x[i]
        pandas_table[i][2] = y[i]
        pandas_table[i][3] = z[i]
        pandas_table[i][4] = error[i]
    # (Optional) Rename the columns to something more readable:
    pandas_table.columns = ["x", "y", "z", "time"]

    # Write DataFrame to CSV
    pandas_table.to_csv(csv_pandastable, index=False)

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
    rows = len(time)
    columns = 1
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)

    for i in range(len(time)):
        pandas_table[i][0] = time[i]

    return pandas_table

################################################################################################################

'''linear algebra stuff'''

def convert_coordinates(start:tuple,end:tuple, coord:tuple)->tuple:
    '''
    converts the coordinate into a new coordinate system based on the line between start and end
    '''

    vector = np.array(end) - np.array(start) # a vector between start and end

    unit = vector / vector.dot(vector) # the unit vector in that direction

    normal = np.rot90(unit)

    proj_tangent = unit.dot(coord) # gets the projection. I.e. the coordinates in the new system
    proj_normal = normal.dot(coord)

    return proj_tangent, proj_normal 

################################################################################################################

def main():
    
    # add testing code here
    start = [0,0]
    end = [5, 3]
    test_coord = [2,1]
    print(convert_coordinates(start,end,test_coord))

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else
