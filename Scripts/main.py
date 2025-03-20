'''
the main function,
to test out stuff

'''

import Handling_ALL_Functions
import Data_LT_importer

# Code to call the function multiple times.
def repeat_function(func, n):
    for i in range(n):
        func()
repeat_function(Handling_ALL_Functions.handle_LT, 3)


# get cool data
table = Handling_ALL_Functions.handle_LT(Data_LT_importer._get_laser_tracker_raw(3))

print(table)

