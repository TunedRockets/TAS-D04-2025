import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Handling_ALL_Functions import get_processed_data

'''Here you can find the code to get meaningful statistical values 
    and the function  to plot the histograms of the four type of errors
    Written by: Manuel Cruz, Diogo Ying.'''


for i in range(1,33):
    processed_data = get_processed_data(tow=i, sensor_type= "LLS_A", overwrite=False)
    processed_data.columns = ["time", "width", "center",  "error_LLS_A"]
    print(processed_data)



#Here we obtain the mean, median, standard deviation, minimum and maximum
# of the four error types.
'''Note: It might be necessary to change the names of the errors when calling the DataFrame 'data'.
    For example: In the below function, I call data['error_LLS_A'],
    but the name in the DataFrame might not be the same!,
    so it may be necessary to change it either in all functions 
    or in the DataFrame where the data is stored!'''
def statistical_values(data: pd.DataFrame):
    # Find the statistical values of the data
    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_CAM']]
    mean = []
    median = []
    std = []
    minimum = []
    maximum = []

    '''We created a For loop to make the code more efficient and readable.
    It goes through all errors (see list 'errors') and appends to a list the 
    necessary statistical values'''
    for error in errors:
        mean.append(round(error.mean(), 4))
        median.append(round(error.median(), 4))   
        std.append(round(error.std(), 4))
        minimum.append(round(error.min(), 4))
        maximum.append(round(error.max(), 4))

    return mean, median, std, minimum, maximum


# Here is the function to plot all types of errors in histograms.
# They all appear in the same figure, in subplots.
'''Note: It might be necessary to change the names of the errors when calling the DataFrame 'data'.
    For example: In the below function, I call data['error_LLS_A'],
    but the name in the DataFrame might not be the same!,
    so it may be necessary to change it either in all functions 
    or in the DataFrame where the data is stored!'''
def plot_histograms(data: pd.DataFrame, title: str):
    # Plot the error of each sensor vs. time
    
    ''' error_LLS_A = LLS A
        error_LLS_B = LLS B
        error_LT = Laser tracker 
        error_camera = camera'''
    
    # Create a 2x2 grid (ax) to subplots
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))  
    fig.suptitle(title)  # Set main title for the figure

    # Created lists for the parameters I need in the for loop, because we cannot say 
    # for e.g. data['error_LLS_A'] in a for loop (it has to have an associated number)
    # and in lists you can refer to strings and so on as a number (the index)!
    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_CAM']]
    errors_names = ['error_LLS_A', 'error_LLS_B', 'error_LT','error_CAM']
    titles = ['Error LLS A vs. time', 
              'Error LLS B vs. time',
              'Error Laser Tracker vs. time',
              'Error Camera vs. time']
    
    # Algorithm to make the code more readable than hard-code every plot (see below)
    for i, error in enumerate(errors):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        # Just plotting and creating titles and labels for the plots
        ax[row, col].hist(error, bins= 20, color='skyblue', edgecolor='black')
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(errors_names[i])
        ax[row, col].set_ylabel('Frequency')
 


'''Example to check if the first function (statistical_values) works'''

'''
# Generating random test data
np.random.seed(42) 
data_size = 100  

data = pd.DataFrame({
    'error_LLS_A': np.random.uniform(0.01, 0.02, data_size),
    'error_LLS_B': np.random.uniform(0.01, 0.02, data_size),
    'error_LT': np.random.uniform(0.01, 0.02, data_size),
    'error_camera': np.random.uniform(0.01, 0.02, data_size),})

# Running the function
stats = statistical_values(data)
print("Mean:", stats[0])
print("Median:", stats[1])
print("Standard Deviation:", stats[2])
print("Min:", stats[3])
print("Max:", stats[4]) '''

