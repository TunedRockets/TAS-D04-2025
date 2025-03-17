import numpy as np
import matplotlib.pyplot as plt

# File path (update to your actual file location)
file_path = r'C:\Study\Aerospace engineering\2. Second Year\Project\AFP\Data Sans Camera\Data Sans Camera\LLS\Straight lines\1\LLS_A_3060_data.csv'

# Load the CSV file into a NumPy array
numpy_array = np.loadtxt(file_path, delimiter=",")

# Split the data into Y and Z coordinates
y_coordinates = numpy_array[:, :2048]  # First 2048 columns (Y values)
z_coordinates = numpy_array[:, 2048:]  # Last 2048 columns (Z values)

# Select a row to process
row_index = 10  # Change this to plot a different row
y_values = y_coordinates[row_index, :]
z_values = z_coordinates[row_index, :]

### STEP 1: REMOVE OUTLIERS USING INTERQUARTILE RANGE (IQR) ###
Q1 = np.percentile(z_values, 25)  # First quartile
Q3 = np.percentile(z_values, 75)  # Third quartile
IQR = Q3 - Q1  # Interquartile range
lower_bound = Q1 - 1.5 * IQR  # Lower bound for outliers
upper_bound = Q3 + 1.5 * IQR  # Upper bound for outliers
#ok
# Create mask to filter out outliers
mask = (z_values >= lower_bound) & (z_values <= upper_bound)

# Apply mask to remove outliers
y_cleaned = y_values[mask]
z_cleaned = z_values[mask]

### STEP 2: FILTER ONLY Z VALUES WITHIN 85.5 < Z < 87.5 ###
mask_z = (z_cleaned > 85.5) & (z_cleaned < 87.5)
y_filtered = y_cleaned[mask_z]
z_filtered = z_cleaned[mask_z]

### STEP 3: APPLY MOVING AVERAGE FILTER ###
def moving_average(data, window_size=51):
    """Applies a simple moving average filter to smooth data."""
    return np.convolve(data, np.ones(window_size) / window_size, mode='valid')

# Adjust window size dynamically to avoid errors
window_size = min(51, len(z_filtered) - 1)
if window_size % 2 == 0:
    window_size += 1  # Ensure the window size is odd

z_smoothed = moving_average(z_filtered, window_size)

# Adjust y-values to match the reduced length of z-values
y_smoothed = y_filtered[:len(z_smoothed)]

### CREATE SIDE-BY-SIDE PLOTS ###
fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # Two subplots side by side

# **Left Plot: Original Noisy Data**
axes[0].plot(y_values, z_values, marker='o', linestyle='-', markersize=2, alpha=0.3, color='gray')
axes[0].set_title("Original Noisy Data")
axes[0].set_xlabel("Y Coordinates")
axes[0].set_ylabel("Z Coordinates")
axes[0].grid(True)

# **Right Plot: Smoothed & Filtered Data**
axes[1].plot(y_filtered, z_filtered, 'o', markersize=3, alpha=0.5, label="Filtered (85.5 < Z < 87.5)", color='blue')
axes[1].plot(y_smoothed, z_smoothed, linestyle='-', linewidth=2, label="Smoothed Curve (Moving Avg)", color='red')
axes[1].set_title("Outlier Removed & Smoothed Data (85.5 < Z < 87.5)")
axes[1].set_xlabel("Y Coordinates")
axes[1].grid(True)
axes[1].legend()

# Display the plots
plt.tight_layout()
plt.show()