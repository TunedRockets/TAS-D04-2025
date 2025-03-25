import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

#@dataclass
#class Model_Regression:
#    bin_error: list     # this is the location of the bin: E_i
#    mean:list           # this is the mean value of the bin: E_i+1
#    variance: list      # this is the variance of the bin: sigma^2?


def fit(data: pd.DataFrame):   #bin_error: np.array, bin_mean: np.array, bin_variance: np.array
    bin_error = np.array(data["x_mean"])
    bin_mean = np.array(data["deviation_mean"])
    bin_variance = np.array(data["deviation_variance"])
    # mean
    mu_a, mu_b, mu_c = get_regression(bin_error, bin_mean)
    plot_function(mu_a, mu_b, mu_c, bin_error, bin_mean, 'mean')

    # variance
    var_a, var_b, var_c = get_regression(bin_error, bin_variance)
    plot_function(var_a, var_b, var_c, bin_error, bin_variance, 'variance')

def fit_cubic(data: pd.DataFrame):   #bin_error: np.array, bin_mean: np.array, bin_variance: np.array
    bin_error = np.array(data["x_mean"])
    bin_mean = np.array(data["deviation_mean"])
    bin_variance = np.array(data["deviation_variance"])
    # mean
    mu_a, mu_b, mu_c, mu_d = get_regression_cubic(bin_error, bin_mean)
    plot_function(mu_a, mu_b, mu_c, mu_d, bin_error, bin_mean, 'mean')

    # variance
    var_a, var_b, var_c, var_d = get_regression_cubic(bin_error, bin_variance)
    plot_function(var_a, var_b, var_c, var_d, bin_error, bin_variance, 'variance')


def get_regression(x_cords: np.array, y_cords: np.array):

    X, Y = [], []
    for i in range(len(x_cords)):
        X.append([1, x_cords[i], x_cords[i]**2])
        Y.append(y_cords[i])

        #X = np.array(((1, x_cords[0], x_cords[0]**2), (1, x_cords[1], x_cords[1]**2), (1, x_cords[2], x_cords[2]**2)))
        #Y = np.array((y_cords[0], y_cords[1], y_cords[2]))

    print(X, Y)
    X_T = np.transpose(X)
    inverse_factor = np.linalg.inv(np.matmul(X_T, X))

    Beta = np.matmul(inverse_factor, X_T).dot(Y)

    return Beta[0], Beta[1], Beta[2]    # c, b, a

def get_regression_cubic(x_cords: np.array, y_cords: np.array):

    X, Y = [], []
    for i in range(len(x_cords)):
        X.append([1, x_cords[i], x_cords[i]**2, x_cords[i]**3])
        Y.append(y_cords[i])

        #X = np.array(((1, x_cords[0], x_cords[0]**2), (1, x_cords[1], x_cords[1]**2), (1, x_cords[2], x_cords[2]**2)))
        #Y = np.array((y_cords[0], y_cords[1], y_cords[2]))

    print(X, Y)
    X_T = np.transpose(X)
    inverse_factor = np.linalg.inv(np.matmul(X_T, X))

    Beta = np.matmul(inverse_factor, X_T).dot(Y)

    return Beta[0], Beta[1], Beta[2], Beta[3]    # d, c, b, a


def plot_function(a: float, b: float, c: float, d: float, bin_error: list, bin_mean: list, title: str):     # y = a + bx + cx^2
    points = 101
    min, max = np.min(bin_error), np.max(bin_error)
    start = min - 0.5*(max-min)
    end = max + 0.5*(max-min)
    step = (end - start)/(points-1)

    x_list, y_list = [], []
    for x in np.arange(start, end, step):
        y = a + b*x + c*(x**2) + d*(x**3)

        x_list.append(x)
        y_list.append(y)

    plt.plot(x_list, y_list)
    plt.scatter(bin_error, bin_mean)
    plt.title(title)
    # plt.ylim((min(y_list), max(y_list)))
    plt.show()





def test():
    bin_error = np.array([-2.2, -0.9, 0, 1, 2.1])
    bin_mean = np.array([-1, -0.5, 0, 0.7, 1.1])
    bin_variance = np.array([5, 1.2, 0, 2, 3.8])

    fit(bin_error, bin_mean, bin_variance)


#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from scipy.optimize import curve_fit
#import scipy.stats as stats
#from sklearn.model_selection import train_test_split
#from Data_CAM_importer import CAM_exceltolist
#from scipy.stats import linregress
#
## Load and Prepare Data
#
## Load Excel data using custom importer
#CAM_file_path = r'Data\Data Sans Camera\Camera data\Cameradata_Modified.xlsx'
#all_sheets_data = CAM_exceltolist(CAM_file_path)
#
## Extract 5th column (index 4) from all sheets and combine
#fifth_column_arrays = [
#    sheet_df.iloc[:, 4].dropna().to_numpy() for sheet_df in all_sheets_data
#]
#combined_fifth_column_array = np.concatenate(fifth_column_arrays, axis=0)
#
## Create (x_n, x_{n+1}) pairs
#x_values = combined_fifth_column_array[:-1]
#y_values = combined_fifth_column_array[1:]
#
#
## Split into training and testing ( 50% train, 50% test)
#x_train, x_test, y_train, y_test = train_test_split(
#    x_values, y_values, test_size=0.5, random_state=42
#)
#
## Binning and Averaging on Training Data
#num_bins = 20
#
## Sort training x-values and reorder y-values accordingly
#sorted_indices = np.argsort(x_train)
#x_sorted = x_train[sorted_indices]
#y_sorted = y_train[sorted_indices]
#
## Equal-count bin edges
#bin_edges = np.linspace(0, len(x_sorted), num_bins + 1, dtype=int)
#
## Compute bin-wise averages
#x_binned = [np.mean(x_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
#y_binned = [np.mean(y_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
#
##scatter Plot with Binned Averages and regression model
#slope, intercept, r_value, p_value, std_err = linregress(x_binned, y_binned)
#print(r_value)
#
#plt.figure(figsize=(8, 6))
#plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Data")
#plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
#plt.plot(x_binned, np.array(x_binned) * slope + intercept, color='red', label='Linear Fit')
#plt.xlabel("X (Train)")
#plt.ylabel("Y (Train)")
#plt.title("Scatter Plot with Equal-Count Binning (Train Data)")
#plt.legend()
#plt.grid(True)
#plt.show()
#
## Compute Deviations per Bin
#
#deviations_per_bin = []
#for i in range(num_bins):
#    bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
#    bin_y_values = y_sorted[bin_start:bin_end]
#    bin_x_values = x_sorted[bin_start:bin_end]
#    bin_mean = np.mean(bin_y_values)
#
#    deviations = []
#    for x in range(len(bin_x_values)):
#    # print(bin_y_values, bin_x_values)
#        deviation = bin_y_values[x] - bin_x_values[x]
#        deviations.append(deviation)
#    deviations_per_bin.append(deviations)
#
## Plot Histograms of Deviations per Bin
#
#
#rows, cols = 4, 5
#fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
#fig.suptitle("Histograms of Deviations per Bin (Training Data)", fontsize=16)
#axes = axes.flatten()
#
#for i in range(num_bins):
#    ax = axes[i]
#    bin_devs = deviations_per_bin[i]
#    x_mean = x_binned[i]  # Mean x-value of the bin
#
#    # Histogram of deviations
#    counts, bins, patches = ax.hist(bin_devs, bins=30, edgecolor='black', color='blue', density=True)
#
#    # Fit normal distribution to the deviations
#    mu, std = stats.norm.fit(bin_devs)
#
#    # Generate and plot normal PDF
#    x_fit = np.linspace(min(bin_devs), max(bin_devs), 100)
#    p_fit = stats.norm.pdf(x_fit, mu, std)
#    ax.plot(x_fit, p_fit, 'r', linewidth=2)
#
#    # Annotate with μ, σ, and x̄
#    annotation = f"x_mean = {x_mean:.4f}\nμ = {mu:.4f}\nσ = {std:.4f}"
#    ax.text(0.95, 0.95, annotation, transform=ax.transAxes,
#            verticalalignment='top', horizontalalignment='right',
#            fontsize=10, bbox=dict(facecolor='white'))
#
#    # Customize axes
#    ax.set_title(f"Bin {i}")
#    ax.set_xlabel("Deviation")
#    ax.set_ylabel("Density")
#    ax.grid(True)
#
## Final layout adjustments
#plt.tight_layout(rect=[0, 0, 1, 1])
#plt.show()
#
#
##-------------------------
##summarize all data
##-------------------------
#
#bin_stats = []
#
#for i in range(num_bins):
#    bin_devs = deviations_per_bin[i]
#    x_mean = x_binned[i]
#    y_mean = y_binned[i]
#    mu, std = stats.norm.fit(bin_devs)
#    variance = std**2
#
#    bin_stats.append({
#        "x_mean": x_mean,
#        "y_mean": y_mean,
#        "deviation_mean": mu,
#        "deviation_variance": variance
#})
#
## Convert to DataFrame for easy viewing
#bin_stats_df = pd.DataFrame(bin_stats)
#
## Display the table
#print(bin_stats_df)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from Data_CAM_importer import CAM_exceltolist
from Handling_ALL_Functions import get_processed_data

# Prepare an empty list to store (x_n, x_{n+1}) pairs for each tow
all_pairs = []

# Loop through tow numbers from 1 to 31
for tow_number in range(1, 32):
    # Get processed data for the current tow and "LT" type
    tow_data = get_processed_data(tow_number, "LT")

    # Ensure that the returned object is a dataframe
    if not tow_data.empty and tow_data.shape[1] > 1:  # Ensure there are at least two columns
        # Extract the second-to-last column
        second_to_last_column = tow_data.iloc[:, -1].values  # Convert to numpy array

        # Create (x_n, x_{n+1}) pairs for the current tow
        x_values = second_to_last_column[:-1]
        y_values = second_to_last_column[1:]

        # Append pairs as a list of tuples
        all_pairs.extend(zip(x_values, y_values))

# After processing all tows, convert collected pairs into numpy arrays
all_pairs = np.array(all_pairs)
x_values = all_pairs[:, 0]
y_values = all_pairs[:, 1]


# Train-Test Split

# Split into training and testing ( 50% train, 50% test)
x_train, x_test, y_train, y_test = train_test_split(
    x_values, y_values, test_size=0.5, random_state=42
)

# Binning and Averaging on Training Data

num_bins = 20

# Sort training x-values and reorder y-values accordingly
sorted_indices = np.argsort(x_train)
x_sorted = x_train[sorted_indices]
y_sorted = y_train[sorted_indices]

# Equal-count bin edges
bin_edges = np.linspace(0, len(x_sorted), num_bins + 1, dtype=int)

# Compute bin-wise averages
x_binned = [np.mean(x_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
y_binned = [np.mean(y_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]

# catter Plot with Binned Averages

plt.figure(figsize=(8, 6))
plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Data")
plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
plt.xlabel("X (Train)")
plt.ylabel("Y (Train)")
plt.title("Scatter Plot with Equal-Count Binning (Train Data)")
plt.legend()
plt.grid(True)
plt.show()

# Compute Deviations per Bin

deviations_per_bin = []
for i in range(num_bins):
    bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
    bin_y_values = y_sorted[bin_start:bin_end]
    bin_x_values = x_sorted[bin_start:bin_end]
    bin_mean = np.mean(bin_y_values)

    deviations = []
    for x in range(len(bin_x_values)):
    # print(bin_y_values, bin_x_values)
        deviation = bin_y_values[x] - bin_x_values[x]
        deviations.append(deviation)
    deviations_per_bin.append(deviations)

# Plot Histograms of Deviations per Bin


rows, cols = 4, 5
fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
fig.suptitle("Histograms of Deviations per Bin (Training Data)", fontsize=16)
axes = axes.flatten()

for i in range(num_bins):
    ax = axes[i]
    bin_devs = deviations_per_bin[i]
    x_mean = x_binned[i]  # Mean x-value of the bin

    # Histogram of deviations
    counts, bins, patches = ax.hist(bin_devs, bins=30, edgecolor='black', color='blue', density=True)

    # Fit normal distribution to the deviations
    mu, std = stats.norm.fit(bin_devs)

    # Generate and plot normal PDF
    x_fit = np.linspace(min(bin_devs), max(bin_devs), 100)
    p_fit = stats.norm.pdf(x_fit, mu, std)
    ax.plot(x_fit, p_fit, 'r', linewidth=2)

    # Annotate with μ, σ, and x̄
    annotation = f"x_mean = {x_mean:.4f}\nμ = {mu:.4f}\nσ = {std:.4f}"
    ax.text(0.95, 0.95, annotation, transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='right',
            fontsize=10, bbox=dict(facecolor='white'))

    # Customize axes
    ax.set_title(f"Bin {i}")
    ax.set_xlabel("Deviation")
    ax.set_ylabel("Density")
    ax.grid(True)

# Final layout adjustments
plt.tight_layout(rect=[0, 0, 1, 1])
plt.show()


#-------------------------
#summarize all data
#-------------------------

bin_stats = []

for i in range(num_bins):
    bin_devs = deviations_per_bin[i]
    x_mean = x_binned[i]
    y_mean = y_binned[i]
    mu, std = stats.norm.fit(bin_devs)
    variance = std**2

    bin_stats.append({
        "x_mean": x_mean,
        "y_mean": y_mean,
        "deviation_mean": mu,
        "deviation_variance": variance
})

# Convert to DataFrame for easy viewing
bin_stats_df = pd.DataFrame(bin_stats)

# Display the table
print(bin_stats_df)


x = fit_cubic(bin_stats_df)
# x = test()
