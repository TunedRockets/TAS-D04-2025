import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# TODO: find the statistical values (mean, median, std, min, max) of the data
# TODO: Create histograms of the four error types

def statistical_values(data: pd.DataFrame):
    # Find the statistical values of the data
    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_camera']]
    mean = []
    median = []
    std = []
    minimum = []
    maximum = []

    for error in errors:
        mean.append(round(error.mean(), 4))
        median.append(round(error.median(), 4))   
        std.append(round(error.std(), 4))
        minimum.append(round(error.min(), 4))
        maximum.append(round(error.max(), 4))

    return mean, median, std, minimum, maximum

# Generating synthetic test data
np.random.seed(42)  # For reproducibility
data_size = 100  # Number of data points

data = pd.DataFrame({
    'error_LLS_A': np.random.uniform(0.01, 0.02, data_size),
    'error_LLS_B': np.random.uniform(0.01, 0.02, data_size),
    'error_LT': np.random.uniform(0.01, 0.02, data_size),
    'error_camera': np.random.uniform(0.01, 0.02, data_size),})


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
    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_camera']]
    errors_names = ['error_LLS_A', 'error_LLS_B', 'error_LT','error_camera']
    titles = ['Error LLS A vs. time', 
              'Error LLS B vs. time',
              'Error Laser Tracker vs. time',
              'Error camera vs. time']
    
    # Algorithm to make the code more readable than hard-code every plot (see below)
    for i, error in enumerate(errors):
        row = i // 2  # Determine the row (0 or 1)
        col = i % 2   # Determine the column (0 or 1)

        # Just plotting and creating titles and labels for the plots
        ax[row, col].hist(error, bins= 20, color='skyblue', edgecolor='black')
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(errors_names[i])
        ax[row, col].set_ylabel('Frequency')
 


'''Example

# Running the function
stats = statistical_values(data)
print("Mean:", stats[0])
print("Median:", stats[1])
print("Standard Deviation:", stats[2])
print("Min:", stats[3])
print("Max:", stats[4]) '''

