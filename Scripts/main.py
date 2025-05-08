'''
the main function,
to test out stuff

'''
import time
import Handling_ALL_Functions
from Model_ALL_ConsecutiveModeler import tow_visualizer

# code to get all the data into .pkl
# runs all the data and overwrites everything.
start = time.time()
# Handling_ALL_Functions.purge_cache() # argument is false so nobody accidentally does this (:
# Handling_ALL_Functions.create_cache()
# Handling_ALL_Functions.create_processed_cache()
print(f"elapsed time: {time.time() - start} (s)")
# will take some time to run