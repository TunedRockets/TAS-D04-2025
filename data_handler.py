"""
for getting data from wherever we save it, and saving the data in that place

not the sorting, importing, or parsing. 

"""

import numpy as np
import pandas as pd

from constants import z_ref

################################################################################################################
"""Functions for Laser Tracker"""

def handle_LT(time: list, x: list, y: list, z: list, tow: int) -> pd.DataFrame:
    """"This function takes the processed data and
        creates new data points for each time stamp
        where each point in time has a corresponding
        position, and its errors in position"""
    
    rows = len(time)
    columns = 6
    shape = (rows, columns)
    np_array = np.empty(shape)
    pandas_table = pd.DataFrame(np_array)
    error_y, error_z = error_LT(y, z, tow)

    for i in range(len(x)):
        pandas_table[i][0] = time[i]
        pandas_table[i][1] = x[i]
        pandas_table[i][2] = y[i]
        pandas_table[i][3] = z[i]
        pandas_table[i][4] = error_y[i]
        pandas_table[i][5] = error_z[i]
    # (Optional) Rename the columns to something more readable:
    pandas_table.columns = ["time", "x", "y", "z", "y error", "z error"]

    return pandas_table

def error_LT(y: list, z: list, tow_number)->list:
    error_y = []
    error_z = []
    
    y_ref = 125 + 12.5*(tow_number-1)

    for i in range(len(y)):
        error_y.append(y[i] - y_ref)
        error_z.append(z[i] - z_ref)

    return error_y, error_z

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


###############################################################################################
"""saving and loading data"""

_save_path = "Processed data\\"

def save_table(data_table:pd.DataFrame, short_name:str)-> None:
    '''
    saves a pandas dataframe as a ., it will be saved with the short name, use that to access it 
    '''
    data_table.to_pickle(_save_path + short_name + ".pkl")
    # note! this does not save headers or indexes. might need to change that depending on how we do
    return



def load_table(short_name:str)->pd.DataFrame:
    '''
    reads a csv and turns it into a panda Dataframe. access it with the same name used in the save_csv() function
    if file doesn't exist it returns none
    '''
    try:
        return pd.read_pickle(_save_path + short_name + ".pkl")
    except FileNotFoundError:
        return None

def export_to_csv(data_table:pd.DataFrame, name:str)-> None:
    '''
    exports the table to CSV.\n
    Note! if you want to save your progress, use the save_table() function instead,\n
    as the CSV is not reversibly saved (metadata is lost)
    '''
    data_table.to_csv(_save_path + name)
    return None

def get_processed_data(tow:int, type:str, overwrite=False)->pd.DataFrame:
    '''
    Load the processed data, grabbing it from raw if it does not yet exist
    the type specifies what data to grab.
    use the keys: "LT","LLS1","LLS2","CAM"
    if overwrite is true, it will grab from the raw regardless if data exists.
    '''
    # generate consistent name:
    # first check if key is valid
    if type not in ["LS","LLS1","LLS2","CAM"]:
        raise KeyError("No such data exists")
    # then that tow exists:
    if type not in range(1,32):
        raise IndexError("Tow ID out of range")
    # set the name
    name = type + "_" + str(tow)

    # check if file exists:
    if data := load_table(name) and not overwrite:
        #if true the data already exists, return it:
        return data
    # else the data doesn't exist, grab it
    match type:
        case "LT":
            # Laser Tracker
            data = ... # ADD THE LT DATA HERE
            processesed_data = handle_LT(*data)
            save_table(processesed_data, name) # save the data
            return processesed_data
        case "CAM":
            # Camera Data
            data = ... # ADD THE CAM DATA HERE
            processesed_data = handle_camera(*data)
            save_table(processesed_data, name) # save the data
            return processesed_data
        case "LLS1":
            # Laser Line Sensor 1
            data = ... # ADD THE LLS1 DATA HERE
            processesed_data = handle_LLS(*data)
            save_table(processesed_data, name) # save the data
            return processesed_data
        case "LLS2":
            # Laser Line Sensor 2
            data = ... # ADD THE LLS2 DATA HERE
            processesed_data = handle_LLS(*data)
            save_table(processesed_data, name) # save the data
            return processesed_data




################################################################################################################

def main():
    
    # add testing code here
    foo = pd.DataFrame([[1,1,1], [1,2,3], ["hello", "world", "!"]])
    foo.index = ["ones", "range", "strings"]
    foo.columns = [1,2,3]

    print(foo)
    save_table(foo, "test")

    bar = load_table("blard")
    print(bar)

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else
