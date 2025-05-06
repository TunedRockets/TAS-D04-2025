import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from scipy.stats import linregress
from Handling_ALL_Functions import get_synced_data
import math
from scipy.stats import truncnorm
from scipy.interpolate import interp1d

def consecutive_error(sensor, test_ratio=0.8, num_bins=20, random_state=42, bins_show=False, plot_fit=True):
    if sensor not in ["LT", "CAM", "LLS_A", "LLS_B"]:
        raise ValueError("Invalid sensor type. Possible values are 'LT', 'CAM', 'LLS_A', and 'LLS_B'.")

    column = -2 if sensor in ["CAM", "LT"] else -1
    all_pairs = []

    for tow_number in range(1, 32):
        tow_data_bef = get_synced_data(tow_number, spacesynced = True)

        if sensor == "LT":
            tow_data = tow_data_bef[["time", "x", "y", "z", "error_LT", "z error"]]
        elif sensor == "LLS_A":
            tow_data = tow_data_bef[["time", "width_LLS_A", "center_LLS_A", "width error_LLS_A"]]
        elif sensor == "LLS_B":
            tow_data = tow_data_bef[["time", "width_LLS_B", "center_LLS_B", "width_LLS_B"]]
        elif sensor == "CAM":
            tow_data = tow_data_bef[["time", "width_CAM", "center_CAM", "error_CAM"]]

        if not tow_data.empty and tow_data.shape[1] > 1:
            values = tow_data.iloc[:, column].values
            x_values = values[:-1]
            y_values = values[1:]
            all_pairs.extend(zip(x_values, y_values))

    all_pairs = np.array(all_pairs)
    x_values = all_pairs[:, 0]
    y_values = all_pairs[:, 1]

    x_train, x_test, y_train, y_test = train_test_split(x_values, y_values, test_size=test_ratio, random_state=random_state)

    sorted_indices = np.argsort(x_train)
    x_sorted = x_train[sorted_indices]
    y_sorted = y_train[sorted_indices]

    bin_edges = np.linspace(0, len(x_sorted), num_bins + 1, dtype=int)
    x_binned = [np.mean(x_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
    y_binned = [np.mean(y_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]

    slope, intercept, r_value, p_value, std_err = linregress(x_binned, y_binned)

    if plot_fit:
        plt.figure(figsize=(8, 6))
        plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Set")
        plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
        plt.plot(x_binned, np.array(x_binned) * slope + intercept, color='red', label='Linear Fit')
        plt.title(f"{sensor} error correlation")
        plt.legend()
        plt.grid(True)
        plt.show()

    deviations_per_bin = []
    for i in range(num_bins):
        bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
        bin_x_values = x_sorted[bin_start:bin_end]
        bin_y_values = y_sorted[bin_start:bin_end]
        predicted_y_values = slope * bin_x_values + intercept
        deviations = bin_y_values - predicted_y_values
        deviations_per_bin.append(deviations)

    bin_stats = []
    for i in range(num_bins):
        bin_devs = deviations_per_bin[i]
        x_mean = x_binned[i]
        y_mean = y_binned[i]
        mu, std = stats.norm.fit(bin_devs)
        bin_stats.append({"x_mean": x_mean, "y_mean": y_mean, "deviation_mean": mu, "deviation_variance": std**2})

    bin_stats_df = pd.DataFrame(bin_stats)
    return bin_stats_df, slope, intercept, r_value, p_value, std_err, x_sorted, bin_edges, deviations_per_bin

def generate_error_path(start_error, n_steps, slope, intercept, x_sorted, bin_edges, deviations_per_bin, random_seed=0, use_truncnorm=False, oversample=3):
    np.random.seed(random_seed)
    oversampled_steps = oversample * n_steps
    error_path = [start_error]
    x_current = start_error

    for _ in range(oversampled_steps):
        y_pred = slope * x_current + intercept

        bin_index = None
        for i in range(len(bin_edges) - 1):
            bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
            if x_sorted[bin_start] <= x_current <= x_sorted[bin_end - 1]:
                bin_index = i
                break
        if bin_index is None:
            bin_index = 0 if x_current < x_sorted[0] else len(bin_edges) - 2

        deviations = deviations_per_bin[bin_index]
        mu, sigma = stats.norm.fit(deviations)
        sampled_deviation = truncnorm(-2, 2, loc=mu, scale=sigma).rvs() if use_truncnorm else np.random.normal(mu, sigma)
        next_error = y_pred + sampled_deviation
        error_path.append(next_error)
        x_current = next_error

    error_path = np.array(error_path)
    averaged_path = [np.mean(error_path[i * oversample:(i + 1) * oversample]) for i in range(n_steps)]
    averaged_path.insert(0, start_error)
    return np.array(averaged_path)

def generate_avg_simulated_vs_real(
    n_real_tow=1,
    n_runs=100,
    test_ratio=0.5,
    num_bins=100,
    bins_show=False,
    smoothing_window=3,
    interpolation_factor=10
):
    # Train models
    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_cam, bins_cam, devs_cam = consecutive_error(
        "CAM", test_ratio, num_bins=num_bins, bins_show=bins_show, plot_fit=False)
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_lt, bins_lt, devs_lt = consecutive_error(
        "LT", test_ratio, num_bins=num_bins, bins_show=bins_show, plot_fit=False)
    bin_stats_w, slope_w, intercept_w, _, _, _, x_w, bins_w, devs_w = consecutive_error(
        "LLS_B", test_ratio, num_bins=num_bins, bins_show=bins_show, plot_fit=False)

    # Load real tow
    real_data = get_synced_data(tow=n_real_tow, spacesynced = True)
    n_steps = len(real_data) - 1

    real_cam = real_data["center_CAM"].values
    real_lt = real_data["error_LT"].values
    real_width = real_data["width_LLS_B"].values
    real_offset = real_cam + real_lt

    # Store all simulated runs first
    all_cam = np.zeros((n_runs, n_steps + 1))
    all_lt = np.zeros((n_runs, n_steps + 1))
    all_width = np.zeros((n_runs, n_steps + 1))

    for i in range(n_runs):
        all_cam[i] = generate_error_path(real_cam[0], n_steps, slope_cam, intercept_cam, x_cam, bins_cam, devs_cam, random_seed=i)
        all_lt[i] = generate_error_path(real_lt[0], n_steps, slope_lt, intercept_lt, x_lt, bins_lt, devs_lt, random_seed=i)
        all_width[i] = generate_error_path(real_width[0], n_steps, slope_w, intercept_w, x_w, bins_w, devs_w, random_seed=i) + 6.35

    # Take average across runs (axis=0 is seed)
    avg_cam = np.mean(all_cam, axis=0)
    avg_lt = np.mean(all_lt, axis=0)
    avg_width = np.mean(all_width, axis=0)
    avg_offset = avg_cam + avg_lt

    # Interpolate to higher resolution
    steps = np.arange(n_steps + 1)
    interp_steps = np.linspace(0, n_steps, num=(n_steps + 1) * interpolation_factor)

    interp_avg_cam = interp1d(steps, avg_cam, kind='linear')(interp_steps)
    interp_avg_lt = interp1d(steps, avg_lt, kind='linear')(interp_steps)
    interp_avg_width = interp1d(steps, avg_width, kind='linear')(interp_steps)
    interp_avg_offset = interp_avg_cam + interp_avg_lt

    # Smooth by averaging over a window around each real data point
    def smooth_data(interp_data):
        smoothed = []
        half_window = smoothing_window // 2
        for i in range(n_steps + 1):
            center = i * interpolation_factor
            start = max(center - half_window, 0)
            end = min(center + half_window + 1, len(interp_data))
            smoothed.append(np.mean(interp_data[start:end]))
        return np.array(smoothed)

    smooth_avg_cam = smooth_data(interp_avg_cam)
    smooth_avg_lt = smooth_data(interp_avg_lt)
    smooth_avg_width = smooth_data(interp_avg_width)
    smooth_avg_offset = smooth_data(interp_avg_offset)

    # Compute boundaries
    simulated_upper_boundary = smooth_avg_offset + 0.5 * smooth_avg_width
    simulated_lower_boundary = smooth_avg_offset - 0.5 * smooth_avg_width
    real_upper_boundary = real_offset + 0.5 * real_width
    real_lower_boundary = real_offset - 0.5 * real_width

    # Plot comparisons
    fig, axs = plt.subplots(4, 1, figsize=(12, 16), sharex=True)

    axs[0].plot(real_cam, label="Real CAM", color="red")
    axs[0].plot(smooth_avg_cam, label="Avg Sim CAM", color="blue")
    axs[0].set_ylabel("Error [mm]")
    axs[0].set_title("CAM Error")
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(real_lt, label="Real LT", color="red")
    axs[1].plot(smooth_avg_lt, label="Avg Sim LT", color="blue")
    axs[1].set_ylabel("Error [mm]")
    axs[1].set_title("LT Error")
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(real_offset, label="Real Offset", color="red")
    axs[2].plot(smooth_avg_offset, label="Avg Sim Offset", color="blue")
    axs[2].set_ylabel("Offset [mm]")
    axs[2].set_title("Total Offset")
    axs[2].legend()
    axs[2].grid(True)

    axs[3].plot(real_width, label="Real Width LLS_B", color="red")
    axs[3].plot(smooth_avg_width, label="Avg Sim Width LLS_B", color="blue")
    axs[3].set_ylabel("Width [mm]")
    axs[3].set_xlabel("Step")
    axs[3].set_title("Tow Width (LLS_B)")
    axs[3].legend()
    axs[3].grid(True)

    plt.tight_layout()
    plt.show()

    # Overlay plot with upper/lower boundaries
    plt.figure(figsize=(12, 5))
    plt.plot(smooth_avg_offset, label="Total Offset Simulated", c="b")
    plt.plot(simulated_upper_boundary, label="Upper Boundary Simulated", c="b", linestyle='--')
    plt.plot(simulated_lower_boundary, label="Lower Boundary Simulated", c="b", linestyle='--')
    plt.plot(real_offset, label="Real Total Offset", c="r")
    plt.plot(real_upper_boundary, label="Real Upper Boundary", c="r", linestyle='--')
    plt.plot(real_lower_boundary, label="Real Lower Boundary", c="r", linestyle='--')
    plt.xlabel("Step")
    plt.ylabel("Error")
    plt.title("Simulated Machine Error Path Over Time")
    plt.grid(True)
    plt.legend()
    plt.show()

    # Print error metric
    mse_cam = np.mean((real_cam - smooth_avg_cam) ** 2)
    print(f"\nMean Squared Error (CAM): {mse_cam:.2f}")

if __name__ == "__main__":
    generate_avg_simulated_vs_real(
        n_real_tow=1,
        n_runs=100,
        test_ratio=0.5,
        num_bins=100,
        bins_show=False,
        smoothing_window=3,
        interpolation_factor=10
    )