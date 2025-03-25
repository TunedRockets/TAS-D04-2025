#We input our current error, which we will call x
# we calculate the mean of the next error, which we call y from the regression model
#the value of x, the previous error, corresponds to a certain bin which contains a normal curve the randomness in the deviation of y 
#we extract a random point from the normal curve 
#we add this value to the before calculated mean

#Note: we cant create a value of the mean or the histogram/normal curve of the devation for a certain data point of x(previous error), 
#       because we don’t have enough data points at that precise point. This is why bins have been created: 
#       this works, but will obtain a slight bias, because the deviation normal curve does not 
#       correspond to the exact value of x, but only to the values around it

    

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from Data_CAM_importer import CAM_exceltolist
from scipy.stats import linregress

# Load and Prepare Data

# Load Excel data using custom importer
CAM_file_path = r'Data\Data Sans Camera\Camera data\Cameradata_Modified.xlsx'
all_sheets_data = CAM_exceltolist(CAM_file_path)

# Extract 5th column (index 4) from all sheets and combine
fifth_column_arrays = [
    sheet_df.iloc[:, 4].dropna().to_numpy() for sheet_df in all_sheets_data
]
combined_fifth_column_array = np.concatenate(fifth_column_arrays, axis=0)

# Create (x_n, x_{n+1}) pairs
x_values = combined_fifth_column_array[:-1]
y_values = combined_fifth_column_array[1:]


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

#scatter Plot with Binned Averages and regression model
slope, intercept, r_value, p_value, std_err = linregress(x_binned, y_binned)
print(r_value)

plt.figure(figsize=(8, 6))
plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Data")
plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
plt.plot(x_binned, np.array(x_binned) * slope + intercept, color='red', label='Linear Fit')
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

    # Get x and y values in this bin
    bin_x_values = x_sorted[bin_start:bin_end]
    bin_y_values = y_sorted[bin_start:bin_end]

    # Predict y-values using regression model
    predicted_y_values = slope * bin_x_values + intercept

    # Compute deviation (residuals) at each point
    deviations = bin_y_values - predicted_y_values
    deviations_per_bin.append(deviations)
# Plot Histograms of Deviations per Bin


rows, cols = 4, 5
fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
fig.suptitle("Histograms of Deviations per Bin (Training Data)", fontsize=16)
axes = axes.flatten()

for i in range(num_bins):
    ax = axes[i]
    bin_devs = deviations_per_bin[i]
    bin_x_values = x_sorted[bin_edges[i]:bin_edges[i + 1]]

    # Histogram of deviations
    counts, bins, patches = ax.hist(bin_devs, bins=30, edgecolor='black', color='blue', density=True)

    # Fit normal distribution to the deviations
    mu, std = stats.norm.fit(bin_devs)

    # Generate and plot normal PDF
    x_fit = np.linspace(min(bin_devs), max(bin_devs), 100)
    p_fit = stats.norm.pdf(x_fit, mu, std)
    ax.plot(x_fit, p_fit, 'r', linewidth=2)

    # Compute bin x-range
    x_min = np.min(bin_x_values)
    x_max = np.max(bin_x_values)

    # Annotate with x bounds, μ and σ
    annotation = f"x ∈ [{x_min:.2f}, {x_max:.2f}]\nμ = {mu:.4f}\nσ = {std:.4f}"
    ax.text(0.95, 0.95, annotation, transform=ax.transAxes,
            verticalalignment='top', horizontalalignment='right',
            fontsize=10, bbox=dict(facecolor='white'))

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


