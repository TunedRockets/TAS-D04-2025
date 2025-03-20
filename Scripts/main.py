'''
the main function,
to test out stuff

'''

import Handling_ALL_Functions

# code to get all the data into .pkl
# runs all the data and overwrites

codes = ["LT","LLS1","LLS2","CAM"]
tows = range(1,32)

for code in codes:
    for tow in tows:
        Handling_ALL_Functions.get_processed_data(tow,code, True)