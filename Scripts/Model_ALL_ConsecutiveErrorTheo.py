import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from scipy.stats import linregress
from Handling_ALL_Functions import get_processed_data

def consecutive_error(sensor, error='', test_ratio=0.8, random_state=42):
    """
        Analyze consecutive error pairs and their distributions from processed sensor data.

        Parameters
        ----------
        sensor : str
            The type of sensor data to process. This determines which column of data
            is used for analysis.
        error: str
            [ONLY for LT and CAM] Type of error to be analyzed.
            This determines which column of data is used for analysis.
            Possible values are:
            LT: "y" or "z"
            CAM: "width" or "center" ("width" refers to tow width error, "center" refers to tow center error)
            LLS_A or LLS_B: does not matter, input anything.
        test_ratio : float
            Proportion of data to use for testing, ranging from 0.0 to 1.0 (e.g., 0.2 uses
            20% of the data for testing and 80% for training).
        random_state : int
            Is used for the test/train split. Ensures reproducible splits of the data.
            Change it to another integer for a different split, or set it to None for random behavior.

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
    else:  # So for LLS_A, LLS_B, CAM center and LT z
        column = -1

    if sensor == "LLS_A" or sensor == "LLS_B":
        error = ''  # Fixes labeling issues


    # Prepare an empty list to store (x_n, x_{n+1}) pairs for each tow
    all_pairs = []

    # Loop through tow numbers from 1 to 31
    for tow_number in range(1, 32):
        # Get processed data for the current tow and sensor type
        tow_data = get_processed_data(tow_number, sensor)

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

    # Split into training and testing (test_ratio * 100)% of data is used.
    x_train, x_test, y_train, y_test = train_test_split(
        x_values, y_values, test_size=test_ratio, random_state=random_state
    )
    # NOTE: random_state ensures reproducible splits of the data;
    # change it to another integer for a different split, or set it to None for random behavior.

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

    # scatter Plot with Binned Averages and regression model
    slope, intercept, r_value, p_value, std_err = linregress(x_binned, y_binned)
    print(r_value)



    plt.figure(figsize=(8, 6))
    plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Set")
    plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
    plt.plot(x_binned, np.array(x_binned) * slope + intercept, color='red', label='Linear Fit')
    params = {'mathtext.default': 'regular'}
    plt.rcParams.update(params)
    plt.xlabel("$ε_{i}$ [mm]")
    plt.ylabel("$ε_{i+1}$ [mm]")
    plt.title("{} {} : Consecutive Error Correlation (Training set)".format(sensor, error))
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
    fig.suptitle("{} {} : Histograms of Deviations per Bin (Training set)".format(sensor, error))
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
        ax.set_xlabel("Deviation [mm]")
        ax.set_ylabel("Density")
        ax.grid(True)

    # Final layout adjustments
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()

    # -------------------------
    # summarize all data
    # -------------------------

    bin_stats = []

    for i in range(num_bins):
        bin_devs = deviations_per_bin[i]
        x_mean = x_binned[i]
        y_mean = y_binned[i]
        mu, std = stats.norm.fit(bin_devs)
        variance = std ** 2

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

    return bin_stats_df

if __name__ == "__main__":
    # Test your function here
    consecutive_error("CAM", "width", 0.2)
