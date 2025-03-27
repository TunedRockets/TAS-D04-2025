"""
For getting data from wherever we save it, and saving the data in that place

Everything is wrapped up in get_processed_data(), just use that and everything will just work :)
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║  USE GET PROCESSED DATA AND IT DEALS WITH EVERYTHING! ║
║  NO NEED TO DO ANITHING ELSE, IT FIXES EVERYTHING!    ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
"""

import numpy as np
import pandas as pd
import glob
import os

from constants import z_ref
import Data_LLS_AB_importer
import Data_LT_importer
import Data_CAM_importer

################################################################################################################
"""Functions for Laser Tracker"""

def _handle_LT(time: list, x: list, y: list, z: list, tow: int) -> pd.DataFrame:
    """"This function takes the processed data and
        creates new data points for each time stamp
        where each point in time has a corresponding
        position, and its errors in position"""
    
    rows = len(time)
    columns = 6
    shape = (rows, columns)
    pandas_table = np.empty(shape)
    error_y, error_z = _error_LT(y, z, tow)
    zero_time = time_to_float(time[0])

    for i in range(len(x)):
        pandas_table[i][0] = time_to_float(time[i]) - zero_time
        pandas_table[i][1] = x[i]
        pandas_table[i][2] = y[i]
        pandas_table[i][3] = z[i]
        pandas_table[i][4] = error_y[i] # This is the y-error, it is just a better naming
        pandas_table[i][5] = error_z[i]
    # (Optional) Rename the columns to something more readable:
    pandas_table = pd.DataFrame(pandas_table)

    pandas_table.columns = ["time", "x", "y", "z", "error_LT", "z error"]

    return pandas_table

def _error_LT(y: list, z: list, tow_number)->list:
    """"This function takes a given tow path
        and calculates the error between the
        actual path and the intended path"""
    
    error_y = []
    error_z = []

    if tow_number == 1:
        y_ref = 125
    else:
        y_ref = 125 + 12.5 * (tow_number)

    for i in range(len(y)):
        error_y.append(y[i] - y_ref)
        error_z.append(z[i] - z_ref)

    return error_y, error_z

################################################################################################################
"""Functions for Laser Line Scanner"""

def _handle_LLS(time: list, left_edge: list, right_edge: list) -> pd.DataFrame:
    """"This function takes the processed data and
        creates new data points for each time stamp
        where each point in time has a corresponding
        width and its the center of the tow"""
    

    
    rows = len(time)
    columns = 4
    shape = (rows, columns)
    pandas_table = np.empty(shape)
    zero_time = time_to_float(time[0])

    for i in range(len(time)):
        pandas_table[i][0] = time_to_float(time[i]) - zero_time
        pandas_table[i][1] = (right_edge[i] - left_edge[i]) # width
        pandas_table[i][2] = 0.5*(right_edge[i] + left_edge[i]) # center
        pandas_table[i][3] = (pandas_table[i][1]-6.35) # error (6.35 is the right width)
    
    pandas_table = pd.DataFrame(pandas_table)
    pandas_table.columns = ["time", "width", "center","width error"]

    return pandas_table



################################################################################################################
"""Functions for Camera"""

def _handle_camera(time: list, left_edge: list, right_edge: list) -> pd.DataFrame:
    rows = len(time)
    columns = 4
    shape = (rows, columns)
    pandas_table = np.empty(shape)
    zero_time = time_to_float(time[0])

    for i in range(len(time)):
        pandas_table[i][0] = time_to_float(time[i]) - zero_time
        pandas_table[i][1] = (right_edge[i] - left_edge[i]) # width
        pandas_table[i][2] = 0.5 * (right_edge[i] + left_edge[i])
        pandas_table[i][3] = (right_edge[i] - left_edge[i]) - 6.35  # assume width error
    pandas_table = pd.DataFrame(pandas_table)
    pandas_table.columns = ["time", "width", "center", "error_CAM"]

    return pandas_table

################################################################################################################

'''extra stuff'''

def time_to_float(date:str)->float:
    """converts a string into a float of time"""
    date = date.strip("'").split(" ")[1]
    hour, minute, second = date.split(":")
    return float(second) + float(minute) * 60 + float(hour) * 3600




def convert_coordinates(start:tuple,end:tuple, coord:tuple)->tuple:
    '''This function converts the coordinate into a new
        coordinate system based on the line between start and end'''

    vector = np.array(end) - np.array(start) # a vector between start and end

    unit = vector / vector.dot(vector) # the unit vector in that direction

    normal = np.rot90(unit)

    proj_tangent = unit.dot(coord) # gets the projection. I.e. the coordinates in the new system
    proj_normal = normal.dot(coord)

    return proj_tangent, proj_normal 

################################################################################################################
"""saving and loading data"""

_save_path = "Processed data\\"

def _save_table(data_table:pd.DataFrame, short_name:str)-> None:
    '''This function saves a pandas dataframe as
        a .pkl, it will be saved with the short name, 
        use that to access it'''
    
    data_table.to_pickle(_save_path + short_name + ".pkl")
    # note! this does not save headers or indexes. might need to change that depending on how we do
    return

def _load_table(short_name:str)->pd.DataFrame:
    '''This function reads a pkl and turns it into 
        a panda Dataframe. access it with the same name 
        used in the save_csv() function if file doesn't exist it returns none'''
    
    try:
        return pd.read_pickle(_save_path + short_name + ".pkl")
    except FileNotFoundError:
        return None

def export_to_csv(data_table:pd.DataFrame, name:str)-> None:
    '''This function exports the table to CSV.
        Note! if you want to save your progress, use the save_table() function instead,
        as the CSV is not reversibly saved (metadata is lost)'''
    
    data_table.to_csv(_save_path + name)
    return None

def purge_cache(confirmation:bool = False)->None:
    '''gets rid of all the files in the cache.\n
    Warning! don't do this unless you're sure you want to\n
    you will have to generate all the data again'''

    print("purging cache...")
    if confirmation != True:
        raise PermissionError("You did not give confirmation for purging the cache. are you sure you want to do this?")

    files = glob.glob(_save_path + "*")
    for file in files:
        if os.path.isfile(file):
            os.remove(file)
    print("cache purged")

def create_cache()->None:
    """runs through all the datatypes and generates the cache, will take some time"""
    print("Let there be cache...")
    codes = ["LT","LLS_A","LLS_B","CAM"]
    tows = range(1,32)

    for code in codes:
        for tow in tows:
            get_processed_data(tow,code, True)

def get_processed_data(tow:int, sensor_type:str, overwrite=False)->pd.DataFrame:
    '''
    This function handles ALL the grabbing and processing of the raw data\n
    call this and it will do all the stuff for you, no other functions needed\n
    the function parameters are:\n
    \n
    tow:int, the index of the tow from 1 to 32\n
    sensor_type:str, the type of data to get. valid keys are: "LT","LLS_A","LLS_B","CAM"\n
    overwrite:bool (optional), If this is true, the function will ignore the cache\n
    and reprocess the raw data. False by default. only do this if something in the processing\n
    has changed, or if the raw data has changed.
    '''

    # generate consistent name:
    # first check if key is valid
    if sensor_type not in ["LT","LLS_A","LLS_B","CAM"]:
        raise KeyError(f"the Key {sensor_type} was invalid: No such data exists")
    # then that tow exists:
    if tow not in range(1,32):
        raise IndexError(f"Tow ID {tow} is out of range")
    # set the name
    name = sensor_type + "_" + str(tow)

    # check if file exists:
    data = _load_table(name)

    if data is not None and not overwrite:
        #if true the data already exists, return it:
        return data
    # else the data doesn't exist, grab it
    print(f"No file with code {name} cached. Generating new data...")
    match sensor_type:
        case "LT":
            # Laser Tracker
            data = np.array(Data_LT_importer.LT_exceltolist()[tow-1]).T
            processesed_data = _handle_LT(*data[1:], tow)

        case "CAM":
            # Camera Data
            data = np.array(Data_CAM_importer.CAM_exceltolist()[tow-1]).T
            processesed_data = _handle_camera(*data[:3])

        case "LLS_A":
            # Laser Line Sensor 1
            data = np.array(Data_LLS_AB_importer.LLS_exceltoarray()[tow*2-2]).T
            processesed_data = _handle_LLS(*data[:3])

        case "LLS_B":
            # Laser Line Sensor 2
            data = np.array(Data_LLS_AB_importer.LLS_exceltoarray()[tow*2-1]).T
            processesed_data = _handle_LLS(*data[:3])
    _save_table(processesed_data, name) # save the data
    return processesed_data

################################################################################################################

def main():
    # add testing code here
    print(get_processed_data(1,"CAM", True))
    pass


if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else
