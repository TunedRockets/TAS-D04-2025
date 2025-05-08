from Model_ALL_ConsecutiveErrorTheo import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from Handling_ALL_Functions import get_synced_data
import random
import pandas as pd

#starting error distribution can be found here, but is assumed to be uniform based on these graphs ranges of values
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
    plt.figure(figsize=(12, 8))
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

    plt.xlabel("Step (must be converted to x position)")
    plt.ylabel("y position [mm]")
    plt.title(f"Simulated {num_tows}-Tow Layout with Random Start Errors")
    plt.legend(loc="upper right", ncol=2)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    #gaps and overlaps calculation
    #Compute vertical gaps between adjacent tows
    gap_overlap_data = {}

    for i in range(num_tows - 1):
        gap_overlap = bottom_lines[i+1]-top_lines[i]  # vertical space between adjacent tows
        col_name = f"Gap/overlap_Tow{i+1}_Tow{i+2}"
        gap_overlap_data[col_name] = gap_overlap  # shape

    gap_overlap_df = pd.DataFrame(gap_overlap_data)
    gap_df = gap_overlap_df.where(gap_overlap_df > 0)
    overlap_df = gap_overlap_df.where(gap_overlap_df < 0)

    #Area Calculations (unitless)
    topmost_line = top_lines[-1]      # Top edge of highest-numbered tow
    bottommost_line = bottom_lines[0] # Bottom edge of lowest-numbered tow
    total_area = np.trapezoid(topmost_line - bottommost_line)

    total_gap_area = 0.0
    total_overlap_area = 0.0

    for col in gap_overlap_df.columns:
        gap_vals = gap_overlap_df[col].values
        gaps = np.where(gap_vals > 0, gap_vals, 0)
        overlaps = np.where(gap_vals < 0, -gap_vals, 0)  # flip sign for integration
        total_gap_area += np.trapezoid(gaps)
        total_overlap_area += np.trapezoid(overlaps)

    gap_percent = (total_gap_area / total_area) * 100 
    overlap_percent = (total_overlap_area / total_area) * 100 

    print(f"\nTotal layout area (unitless): {total_area:.2f}")
    print(f"Gap area: {total_gap_area:.2f} ({gap_percent:.2f}%)")
    print(f"Overlap area: {total_overlap_area:.2f} ({overlap_percent:.2f}%)")

    return gap_overlap_df, gap_df, overlap_df, gap_percent, overlap_percent
gap_overlap_df, gap_df, overlap_df, gap_percent, overlap_percent = generate_multitow_layout(num_tows=10)

# Plot the gap(s) over steps (not time)
plt.figure(figsize=(12, 5))
for column in gap_overlap_df.columns:
    plt.plot(gap_overlap_df.index, gap_overlap_df[column], label=column)

plt.xlabel("Step")
plt.ylabel("Distance between tows (mm): positive for gap, negative for overlap")
plt.title(f"Vertical Gaps Between Adjacent Tows Over Steps\n"
          f"Gap Area: {gap_percent:.2f}%      Overlap Area: {overlap_percent:.2f}%")
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()







#REAL DATA (!deletes a lot of data!, only use as indicator for percentage of gap overlap)
#
#
def calculate_real_gap_overlap_percentages(num_tows=5, tow_spacing_mm=6.35):
    offsets = np.linspace(-(num_tows - 1) / 2, (num_tows - 1) / 2, num_tows) * tow_spacing_mm
    top_lines = []
    bottom_lines = []

    for tow in range(2, 2 + num_tows):
        df = get_synced_data(tow, spacesynced=True)

        cam = df["center_CAM"].dropna().values
        lt = df["error_LT"].dropna().values
        width = df["width_LLS_B"].dropna().values

        min_len = min(len(cam), len(lt), len(width))
        cam = cam[:min_len]
        lt = lt[:min_len]
        width = width[:min_len]

        centerline = cam + lt
        top = centerline + 0.5 * width + offsets[tow - 2]
        bottom = centerline - 0.5 * width + offsets[tow - 2]

        top_lines.append(top)
        bottom_lines.append(bottom)

    # Compute gaps/overlaps only on valid shared ranges
    gap_overlap_data = {}
    total_gap_area = 0.0
    total_overlap_area = 0.0

    for i in range(num_tows - 1):
        top_i = top_lines[i]
        bottom_next = bottom_lines[i + 1]
        common_len = min(len(top_i), len(bottom_next))

        top_i = top_i[:common_len]
        bottom_next = bottom_next[:common_len]

        gap_overlap = bottom_next - top_i
        col_name = f"Gap/overlap_Tow{i+1}_Tow{i+2}"
        gap_overlap_data[col_name] = gap_overlap

        gaps = np.where(gap_overlap > 0, gap_overlap, 0)
        overlaps = np.where(gap_overlap < 0, -gap_overlap, 0)

        total_gap_area += np.trapezoid(gaps)
        total_overlap_area += np.trapezoid(overlaps)

    #Total layout area between outermost top and bottom lines
    topmost = top_lines[-1]
    bottommost = bottom_lines[0]
    common_len_total = min(len(topmost), len(bottommost))
    total_area = np.trapezoid(topmost[:common_len_total] - bottommost[:common_len_total])

    gap_percent = (total_gap_area / total_area) * 100 if total_area > 0 else 0
    overlap_percent = (total_overlap_area / total_area) * 100 if total_area > 0 else 0

    print(f"\n[REAL] Total layout area (unitless): {total_area:.2f}")
    print(f"[REAL] Gap area: {total_gap_area:.2f} ({gap_percent:.2f}%)")
    print(f"[REAL] Overlap area: {total_overlap_area:.2f} ({overlap_percent:.2f}%)")

    return gap_overlap_data, gap_percent, overlap_percent
real_gap_df, real_gap_pct, real_overlap_pct = calculate_real_gap_overlap_percentages(num_tows=30)