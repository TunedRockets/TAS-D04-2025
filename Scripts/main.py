'''
the main function,
to test out stuff

'''
import time
import Handling_ALL_Functions
from Model_ALL_Simulation import generate_multitow_layout

# code to get all the data into .pkl
# runs all the data and overwrites everything.
start = time.time()
# Handling_ALL_Functions.purge_cache() # argument is false so nobody accidentally does this (:
# Handling_ALL_Functions.create_cache()
# Handling_ALL_Functions.create_processed_cache()

num_tows = 1
gap_overlap_df, gap_df, overlap_df, gap_percent, overlap_percent = generate_multitow_layout(num_tows)


print(f"elapsed time: {time.time() - start} (s)")
# will take some time to run