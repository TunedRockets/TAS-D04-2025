import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from scipy.stats import linregress
from Handling_ALL_Functions import get_processed_data
from Handling_ALL_Functions import get_synced_data
import math
from scipy.stats import truncnorm

def consecutive_error(sensor, test_ratio=0.8, num_bins = 20, random_state=42, bins_show = False):
    """
        Analyze consecutive error pairs and their distributions from processed sensor data.

        Parameters
        ----------
        sensor : str
            The type of sensor data to process. This determines which column of data
            is used for analysis.
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

    # Takes care of which column to use
    if sensor == "CAM" or sensor == "LT":
        column = -2
    else:
        column = -1


    # Prepare an empty list to store (x_n, x_{n+1}) pairs for each tow
    all_pairs = []

    # Loop through tow numbers from 1 to 31
    for tow_number in range(1, 10):
        # Get processed data for the current tow and sensor type
        tow_data_bef = get_synced_data(tow_number)

        if sensor == "LT":
            tow_data = tow_data_bef[["time", "x", "y", "z", "error_LT", "z error"]]
        if sensor == "LLS_A":
            tow_data = tow_data_bef[["time", "width_LLS_A", "center_LLS_A", "width error_LLS_A"]]
        if sensor == "LLS_B":
            tow_data = tow_data_bef[["time", "width_LLS_B", "center_LLS_B", "width error_LLS_B"]]
        if sensor == "CAM":
            tow_data = tow_data_bef[["time", "width_CAM", "center_CAM", "error_CAM"]]

        # Ensure that the returned object is a dataframe
        if not tow_data.empty and tow_data.shape[1] > 1:  # Ensure there are at least two columns
            # Extract the last or second-to-last column (based on sensor type)
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

    # Define error label
    error_labels = {"LT": "y error", "CAM": "position error", "LLS_A": "width error", "LLS_B": "width error"}
    error_label = error_labels[sensor]

    # Plot scatter + binned fit
    plt.figure(figsize=(8, 6))
    plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Set")
    plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
    plt.plot(x_binned, np.array(x_binned) * slope + intercept, color='red', label='Linear Fit')
    plt.xlabel("$ε_{i}$ [mm]")
    plt.ylabel("$ε_{i+1}$ [mm]")
    plt.title(f"{sensor} {error_label} : Consecutive Error Correlation (Training set)")
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

    # Paginate histogram grids
    rows, cols = 4, 5
    plots_per_page = rows * cols
    total_bins = num_bins
    total_pages = math.ceil(total_bins / plots_per_page)


    if bins_show:
        for page in range(total_pages):
            start = page * plots_per_page
            end = min(start + plots_per_page, total_bins)

            fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
            fig.suptitle(f"{sensor} {error_label} : Histograms of Deviations per Bin (Page {page + 1}/{total_pages})",
                         fontsize=16)
            axes_flat = axes.flatten()

            for idx_plot in range(start, end):
                bin_idx = idx_plot
                ax = axes_flat[idx_plot - start]
                devs = deviations_per_bin[bin_idx]
                xs = x_sorted[bin_edges[bin_idx]:bin_edges[bin_idx + 1]]

                # Histogram and normal fit
                counts, bins_hist, _ = ax.hist(devs, bins=30, edgecolor='black', density=True)
                mu, std = stats.norm.fit(devs)
                x_fit = np.linspace(devs.min(), devs.max(), 100)
                p_fit = stats.norm.pdf(x_fit, mu, std)
                ax.plot(x_fit, p_fit, 'r', linewidth=2)

                # Annotation
                annotation = f"x ∈ [{xs.min():.2f}, {xs.max():.2f}]\nμ = {mu:.4f}\nσ = {std:.4f}"
                ax.text(0.95, 0.95, annotation, transform=ax.transAxes,
                        verticalalignment='top', horizontalalignment='right', fontsize=10,
                        bbox=dict(facecolor='white', alpha=0.8))

                ax.set_title(f"Bin {bin_idx}")
                ax.set_xlabel("Deviation [mm]")
                ax.set_ylabel("Density")
                ax.grid(True)

            # Turn off unused subplots on last page
            for unused in range(end - start, plots_per_page):
                axes_flat[unused].axis('off')

            plt.tight_layout(rect=[0, 0, 1, 0.96])
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

    return bin_stats_df, slope, intercept, r_value, p_value, std_err, x_sorted, bin_edges, deviations_per_bin

def generate_error_path(start_error, n_steps, slope, intercept, x_sorted, bin_edges, deviations_per_bin, random_seed=0,use_truncnorm=False):
    np.random.seed(random_seed)
    error_path = [start_error]
    x_current = start_error

    for _ in range(n_steps):
        # Predict mean of next error
        y_pred = slope * x_current + intercept

        # Find correct bin
        bin_index = None
        for i in range(len(bin_edges) - 1):
            bin_start = bin_edges[i]
            bin_end = bin_edges[i + 1]
            bin_x_min = x_sorted[bin_start]
            bin_x_max = x_sorted[bin_end - 1]
            if bin_x_min <= x_current <= bin_x_max:
                bin_index = i
                break
        # Use edge bin if out of range
        if bin_index is None:
            bin_index = 0 if x_current < x_sorted[0] else len(bin_edges) - 2

        # Get deviation stats and sample a deviation
        deviations = deviations_per_bin[bin_index]
        mu, sigma = stats.norm.fit(deviations)
        if use_truncnorm:
            # Use truncated normal within ±2σ
            from scipy.stats import truncnorm
            a, b = -2, 2
            sampled_deviation = truncnorm(a, b, loc=mu, scale=sigma).rvs()
        else:
            # Use regular normal distribution
            sampled_deviation = np.random.normal(mu, sigma)
        # Next error
        next_error = y_pred + sampled_deviation
        error_path.append(next_error)
        x_current = next_error

    return np.array(error_path)

if __name__ == "__main__":
    # Test your function here

    bin_stats_df, slope, intercept, r_value, p_value, std_err, x_sorted, bin_edges, deviations_per_bin = consecutive_error("CAM", 0.0001, num_bins=20, bins_show=False)
    bin_stats_df1, slope1, intercept1, r_value1, p_value1, std_err1, x_sorted1, bin_edges1, deviations_per_bin1 = consecutive_error("LT", 0.0001, num_bins=20, bins_show=False)



    synced_data_tow_1 = get_synced_data(tow=2).to_numpy()
    synced_data_cam_tow_1 = synced_data_tow_1[:,13]
    start_error = synced_data_cam_tow_1[0]
    n_steps = len(synced_data_cam_tow_1) - 1
    simulated_tow_path_cam = generate_error_path(
    start_error, n_steps, slope, intercept, x_sorted, bin_edges, deviations_per_bin, random_seed=10
    )

    synced_data_LT_tow_1 = synced_data_tow_1[:,4]
    start_error1 = synced_data_LT_tow_1[0]  
    simulated_tow_path_LT = generate_error_path(
    start_error1, n_steps, slope1, intercept1, x_sorted1, bin_edges1, deviations_per_bin1, random_seed=10
    )
    simulated_total_offset_centerline = simulated_tow_path_LT+simulated_tow_path_cam
    total_offset_real = synced_data_cam_tow_1+synced_data_LT_tow_1

    plt.figure(figsize=(12, 5))
    plt.plot(simulated_tow_path_cam, label="Simulated Error Path CAM")
    plt.plot(synced_data_cam_tow_1,label="real data cam",linestyle="--")
    plt.plot(simulated_tow_path_LT,label="Simulated path LT",linestyle=":")
    plt.plot(simulated_total_offset_centerline, label="Total offset")
    plt.plot(total_offset_real,label="real total offset")
    plt.plot()
    plt.xlabel("Step")
    plt.ylabel("Error")
    plt.title("Simulated Machine Error Path Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()
    MSE=np.sum((synced_data_cam_tow_1- simulated_tow_path_cam) ** 2)
    print("mean squared error is:", MSE)
print(get_synced_data(tow=1))