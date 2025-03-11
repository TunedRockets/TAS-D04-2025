'''
the main function,
to test out stuff

'''

import data_handler
import data_importer



# get cool data
table = data_handler.handle_LT(data_importer._get_laser_tracker_raw(3))


print(table)

