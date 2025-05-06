from Model_ALL_ConsecutiveErrorTheo import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from Handling_ALL_Functions import get_synced_data
import random
import pandas as pd


def fit_starting_error_distribution(sensor: str, plot=True):
    column_map = {
        "CAM": "center_CAM",
        "LT": "error_LT",
        "LLS_A": "width error_LLS_A",
        "LLS_B": "width error_LLS_B"
    }

    col_name = column_map[sensor]
    first_values = []

    for tow in range(2, 32):
        df = get_synced_data(tow, spacesynced=True)

        if col_name in df.columns and not df[col_name].isna().all():
            value = df[col_name].dropna().values[0]  # get first non-NaN value
            first_values.append(value)


    mu, sigma = stats.norm.fit(first_values)

    if plot:
        plt.figure(figsize=(8, 5))
        count, bins, _ = plt.hist(first_values, bins=len(first_values), density=True, edgecolor="black", alpha=0.7, label="Start Values")
        x = np.linspace(min(bins), max(bins), 100)
        plt.plot(x, stats.norm.pdf(x, mu, sigma), 'r--', label=f"Fit: μ={mu:.2f}, σ={sigma:.2f}")
        plt.title(f"Start Error Distribution - {sensor}")
        plt.xlabel("Start Error [mm]")
        plt.ylabel("Density")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    return mu, sigma, first_values




def generate_multitow_layout(num_tows=5,tow_spacing_mm=6.35,n_steps=300,cam_start_range=(-0.4, 0.6),lt_start_range=(-1, -0.8),llsb_start_range=(-0.15, -0.02)):
    # Get binned models
    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
        "CAM", test_ratio=0.5, num_bins=100, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
        "LT", test_ratio=0.5, num_bins=100, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_llsb, slope_llsb, intercept_llsb, _, _, _, x_sorted_llsb, bin_edges_llsb, devs_llsb = consecutive_error(
        "LLS_B", test_ratio=0.5, num_bins=100, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    #get perfect offsets
    offsets = np.linspace(-(num_tows - 1) / 2, (num_tows - 1) / 2, num_tows) * tow_spacing_mm
    plt.figure(figsize=(30, 8))
    #for coloring properly (chatgpt did the plotting)
    cmap = plt.get_cmap("tab10")
    x_vals = np.arange(n_steps)

    top_lines = []
    bottom_lines = []

    for i, offset in enumerate(offsets):
        color = cmap(i % 10)
        start_cam = random.uniform(*cam_start_range)
        start_lt = random.uniform(*lt_start_range)
        start_llsb = random.uniform(*llsb_start_range)

        cam_path = generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                       x_sorted_cam, bin_edges_cam, devs_cam, random_seed=random.randint(0, 10000))
        lt_path = generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                      x_sorted_lt, bin_edges_lt, devs_lt, random_seed=random.randint(0, 10000))
        centerline = offset + cam_path + lt_path

        width_error = generate_error_path(start_llsb, n_steps, slope_llsb, intercept_llsb,
                                          x_sorted_llsb, bin_edges_llsb, devs_llsb, random_seed=random.randint(0, 10000))
        width = width_error + 6.35

        top_line = centerline + 0.5 * width
        bottom_line = centerline - 0.5 * width

        top_lines.append(top_line)
        bottom_lines.append(bottom_line)

        # --- Plot ---
        plt.plot(centerline, color=color, label=f"Tow {i+1} Centerline", linewidth=2)
        plt.plot(top_line, linestyle=":", color=color, linewidth=1)
        plt.plot(bottom_line, linestyle=":", color=color, linewidth=1)
        plt.plot([offset]*n_steps, linestyle="--", color="gray", alpha=0.6,
                 label="Ideal Centerline" if i == 0 else "")

    plt.xlabel("Step")
    plt.ylabel("Position [mm]")
    plt.title(f"Simulated {num_tows}-Tow Layout with Random Start Errors")
    plt.legend(loc="upper right", ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #gaps and overlaps calculation
    # --- Compute vertical gaps between adjacent tows ---
    gap_data = {}

    for i in range(num_tows - 1):
        gap = bottom_lines[i+1]-top_lines[i]  # vertical space between adjacent tows
        col_name = f"Gap/overlap_Tow{i+1}_Tow{i+2}"
        gap_data[col_name] = gap  # shape: (n_steps,)

    gap_df = pd.DataFrame(gap_data)

    return gap_df
a = generate_multitow_layout(num_tows=2)
print(a)
# Plot the gap(s) over time
plt.figure(figsize=(12, 5))
for column in a.columns:
    plt.plot(a.index, a[column], label=column)

plt.xlabel("Timestep")
plt.ylabel("Gap [mm]")
plt.title("Vertical Gaps Between Adjacent Tows Over Time")
plt.axhline(0, color='gray', linestyle='--', linewidth=1)  # Show zero-gap line
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()