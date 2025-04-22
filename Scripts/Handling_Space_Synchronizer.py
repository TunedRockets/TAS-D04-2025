#Imports
from constants import LLS_A_TCP, TCP_LLS_B, roller_diameter
import numpy as np

#Calculate corrected distances
#This step is necessary because the distances are given with respect to the centerpoint of the tool (TCP)
#and the camera does not look at the centerpoint, but a quarter revolution of the compaction roller earlier.
distance_LLS_A_CAM = LLS_A_TCP - np.pi()*roller_diameter*0.25 #corrects distance between LLS_A and CAM
distance_CAM_LLS_B = TCP_LLS_B + np.pi()*roller_diameter*0.25 #corrects distance between CAM and LLS_B
