from Handling_ALL_Functions import get_processed_data
import matplotlib.pyplot as plt

width_velocities = [] # Set up list of velocities
data = get_processed_data(1, "LLS2") # get data, first argument 1-31, second has to stay "LLS2"
widths = data.iloc[:,1] #gets just the width-column
times = data.iloc[:,0]

#Loop over all the data points and store results
for i in range(len(widths)): 
    h = times[i+1] - times[i]
    width_velocity = widths[i] + h * widths[i+1]
    width_velocities.append(width_velocity)

