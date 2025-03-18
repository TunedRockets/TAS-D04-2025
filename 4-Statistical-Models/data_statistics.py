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



'''Example

# Running the function
stats = statistical_values(data)
print("Mean:", stats[0])
print("Median:", stats[1])
print("Standard Deviation:", stats[2])
print("Min:", stats[3])
print("Max:", stats[4]) '''

