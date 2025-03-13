"""

takes the data from the unzipped .zip and turn it into whatever format we pass on
I.e. from the .zip into something to pass on to the data_handler

Author(s): Johannes Nilsson, Martijn van der Voort
"""
#import data_handler
import numpy as np


LINES = 31




# just doing the laser for now as an example
def _get_laser_tracker_raw(line_id:int)->list:
    """
    Get's the laser tracker for the specified line
    """

    # get the path (currently fixed path, so don't move stuff around)
    path_start = "Raw data\Data Sans Camera\Laser tracker\Straight lines"
    path_extension = ".csv"
    path_number = "\\" + str(line_id) + "\\" + str(line_id)
    path = path_start + path_number + path_extension

    # grab the data
    with open(path, "r") as file:
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].split(";") # splits the csv
    
    
    return data

def column_remover_laser_tracker(data_array):
    """Removes unusable data from csv-files"""
    clean_data = np.delete(data_array, [0, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14], axis=1) #Removes columns that 
    return clean_data

def laser_tracker_data_cleaner(file_number):
    """Cleans laser tracker data by removing unnecessary columns and outputting np arrays"""
    data = _get_laser_tracker_raw(file_number) #The argument for this function is the file number you want to clean
    data_array = np.array(data)
    clean_data_laser_tracker = column_remover_laser_tracker(data_array)
    #print(clean_data_laser_tracker) #In real case not necessary to print anything
    return clean_data_laser_tracker
    

#if __name__ == "__main__":
   # main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else