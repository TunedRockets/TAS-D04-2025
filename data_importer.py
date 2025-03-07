"""

takes the data from the unzipped .zip and turn it into whatever format we pass on
I.e. from the .zip into something to pass on to the data_handler

Author(s): Johannes Nilsson,
"""
import data_handler


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


def main():
    
    data = _get_laser_tracker_raw(1)
    for i in range(7):
        print(data[i])

if __name__ == "__main__":
    main() # makes sure this only runs if you run *this* file, not if this file is imported somewhere else