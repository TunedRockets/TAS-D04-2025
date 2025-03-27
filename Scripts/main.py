'''
the main function,
to test out stuff

'''

import Handling_ALL_Functions

# code to get all the data into .pkl
# runs all the data and overwrites everything.
Handling_ALL_Functions.purge_cache() # argument is false so nobody accidentally does this (:
Handling_ALL_Functions.create_cache()
# will take some time to run