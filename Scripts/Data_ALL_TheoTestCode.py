" Nothing here yet but bro is cooking "

#Way the model works: We input our current error, which we will call x
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
from scipy import stats
from sklearn.model_selection import train_test_split
from scipy.stats import linregress
from Data_CAM_importer import CAM_exceltolist
from Handling_ALL_Functions import get_processed_data

def load_and_prepare_data(sensor, error, train_ratio=0.5, random_state=42): #CHANGE USED COLUMN

    """

    Possible sensor values:
    "LT" ; "CAM" ; "LLS_A" ; "LLS_B"

    For LT, specify error, possible values:
    "y" ; "z"

    For CAM, specify error, possible values:
    "width" ; "center"

    """


    # Wrong sensor error message
    if not sensor == "LT" and not sensor == "CAM" and not sensor == "LLS_A" and not sensor == "LLS_B":
        raise ValueError("Invalid sensor type. Possible values are 'LT', 'CAM', 'LLS_A', and 'LLS_B'.")

    # Wrong error type of LT or CAM
    if sensor == "LT" and not error == "y" and not error == "z":
        raise ValueError("Invalid error type for LT sensor. Possible values are 'y' and 'z'.")
    if sensor == "CAM" and not error == "width" and not error == "center":
        raise ValueError("Invalid error type for CAM sensor. Possible values are 'width' and 'center'.")

    # Takes care of error type (for LT and CAM)
    if error == "width" or error == "y":
        column = -2
    else:
        column = -1

    if sensor == "LLS_A" or sensor == "LLS_B":
        column = -1

    # Prepare an empty list to store (x_n, x_{n+1}) pairs for each tow
    all_pairs = []

    # Loop through tow numbers from 1 to 31
    for tow_number in range(1, 32):
        # Get processed data for the current tow and sensor type
        tow_data = get_processed_data(tow_number, sensor, True)

        # Ensure that the returned object is a dataframe
        if not tow_data.empty and tow_data.shape[1] > 1:  # Ensure there are at least two columns
            # Extract the last or second-to-last column (based on error type)
            second_to_last_column = tow_data.iloc[:, column].values  # Convert to numpy array

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

    # Split into training and testing (train_ratio * 100)% of data is used.
    return train_test_split(
        x_values, y_values, test_size=train_ratio, random_state=random_state
    )

def bin_data(x_train, y_train, num_bins):
    sorted_indices = np.argsort(x_train)
    x_sorted = x_train[sorted_indices]
    y_sorted = y_train[sorted_indices]
    bin_edges = np.linspace(0, len(x_sorted), num_bins + 1, dtype=int)
    x_binned = [np.mean(x_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
    y_binned = [np.mean(y_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
    return x_sorted, y_sorted, bin_edges, x_binned, y_binned

def compute_deviations(x_sorted, y_sorted, bin_edges, slope, intercept):
    deviations_per_bin = []
    for i in range(len(bin_edges) - 1):
        bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
        bin_x = x_sorted[bin_start:bin_end]
        bin_y = y_sorted[bin_start:bin_end]
        predicted_y = slope * bin_x + intercept
        deviations = bin_y - predicted_y
        deviations_per_bin.append(deviations)
    return deviations_per_bin

def summarize_bins(x_sorted, y_binned, bin_edges, deviations_per_bin):
    bin_stats = []
    for i in range(len(bin_edges) - 1):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i + 1]
        bin_x_values = x_sorted[bin_start:bin_end]
        y_mean = y_binned[i]
        mu, std = stats.norm.fit(deviations_per_bin[i])
        variance = std**2
        count = bin_end - bin_start
        x_min = np.min(bin_x_values)
        x_max = np.max(bin_x_values)
        x_range_str = f"[{x_min:.2f}, {x_max:.2f}]"
        bin_stats.append({
            "x_range": x_range_str,
            "y_mean": y_mean,
            "deviation_mean": mu,
            "deviation_variance": variance,
            "point_count": count
        })
    return pd.DataFrame(bin_stats)

def predict_next_error(x_value, slope, intercept, x_sorted, bin_edges, deviations_per_bin, confidence):
    y_pred = slope * x_value + intercept
    bin_index = None
    for i in range(len(bin_edges) - 1):
        start_idx = bin_edges[i]
        end_idx = bin_edges[i + 1]
        bin_x_min = x_sorted[start_idx]
        bin_x_max = x_sorted[end_idx - 1]
        if bin_x_min <= x_value <= bin_x_max:
            bin_index = i
            break
    if bin_index is None:
        bin_index = 0 if x_value < x_sorted[0] else len(bin_edges) - 2

    deviations = deviations_per_bin[bin_index]
    deviation_mu, deviation_sigma = stats.norm.fit(deviations)
    adjusted_prediction = y_pred + deviation_mu
    z_score = stats.norm.ppf(1 - (1 - confidence / 100) / 2)
    lower_bound = adjusted_prediction - z_score * deviation_sigma
    upper_bound = adjusted_prediction + z_score * deviation_sigma

    return pd.DataFrame([{"predicted_mean": adjusted_prediction, "lower_bound": lower_bound, "upper_bound": upper_bound, "confidence": confidence,}])

#----------------------------------------------------------
#optional for visualization or something

def plot_regression_with_bins(x_train, y_train, x_binned, y_binned, slope, intercept):
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

def plot_deviation_histograms(x_sorted, bin_edges, deviations_per_bin):
    num_bins = len(deviations_per_bin)
    rows, cols = 5, 8
    fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
    fig.suptitle("Histograms of Deviations per Bin (Training Data)", fontsize=16)
    axes = axes.flatten()
    for i in range(num_bins):
        ax = axes[i]
        bin_devs = deviations_per_bin[i]
        bin_x_values = x_sorted[bin_edges[i]:bin_edges[i + 1]]
        counts, bins, patches = ax.hist(bin_devs, bins=30, edgecolor='black', color='blue', density=True)
        mu, std = stats.norm.fit(bin_devs)
        x_fit = np.linspace(min(bin_devs), max(bin_devs), 100)
        p_fit = stats.norm.pdf(x_fit, mu, std)
        ax.plot(x_fit, p_fit, 'r', linewidth=2)
        x_min = np.min(bin_x_values)
        x_max = np.max(bin_x_values)
        annotation = f"x ∈ [{x_min:.2f}, {x_max:.2f}]\nμ = {mu:.4f}\nσ = {std:.4f}"
        ax.text(0.95, 0.95, annotation, transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right',
                fontsize=10, bbox=dict(facecolor='white'))
        ax.set_title(f"Bin {i}")
        ax.set_xlabel("Deviation")
        ax.set_ylabel("Density")
        ax.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()

#------------------------------------------


# -------------------
# Example usage:
# -------------------
x_train, x_test, y_train, y_test = load_and_prepare_data("LT", "y", 0.5)
x_sorted, y_sorted, bin_edges, x_binned, y_binned = bin_data(x_train, y_train, num_bins=40)
slope, intercept, *_ = linregress(x_binned, y_binned)
deviations_per_bin = compute_deviations(x_sorted, y_sorted, bin_edges, slope, intercept)
bin_stats_df = summarize_bins(x_sorted, y_binned, bin_edges, deviations_per_bin)

plot_regression_with_bins(x_train, y_train, x_binned, y_binned, slope, intercept)
plot_deviation_histograms(x_sorted, bin_edges, deviations_per_bin)

x_input = 0
prediction_df = predict_next_error(x_input, slope, intercept, x_sorted, bin_edges, deviations_per_bin, 99)
print("Prediction result:")
print(prediction_df)
