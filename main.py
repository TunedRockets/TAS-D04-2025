'''
the main function,
to test out stuff

'''

import data_handler
import laser_tracker_data_importer

# Code to call the function multiple times.
def repeat_function(func, n):
    for i in range(n):
        func()
repeat_function(data_handler.handle_LT, 3)


# get cool data
table = data_handler.handle_LT(laser_tracker_data_importer._get_laser_tracker_raw(3))

print(table)

