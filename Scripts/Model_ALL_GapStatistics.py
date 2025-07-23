from Model_ALL_ConsecutiveErrorTheo import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from Handling_ALL_Functions import get_synced_data
import random
import pandas as pd
from Data_ALL_importer import GAP_exceltoarray

steps_per_mm = 0.36


# starting error distribution can be found here, but is assumed to be uniform based on these graphs ranges of values
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
        count, bins, _ = plt.hist(first_values, bins=len(first_values), density=True, edgecolor="black", alpha=0.7,
                                  label="Start Values")
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


def generate_multitow_layout(num_tows=5, tow_spacing_mm=6.35, tow_width_mm=6.35, n_steps=5000,
                             cam_start_range=(-0.4, 0.6), lt_start_range=(-1, -0.8), llsb_start_range=(-0.15, -0.02),
                             plot=True):
    # Get binned models
    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
        "CAM", test_ratio=0.00001, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
        "LT", test_ratio=0.00001, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_llsb, slope_llsb, intercept_llsb, _, _, _, x_sorted_llsb, bin_edges_llsb, devs_llsb = consecutive_error(
        "LLS_B", test_ratio=0.00001, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    # get perfect offsets
    offsets = np.linspace(-(num_tows - 1) / 2, (num_tows - 1) / 2, num_tows) * tow_spacing_mm
    plt.figure(figsize=(12, 8))
    # for coloring properly (chatgpt did the plotting)
    cmap = plt.get_cmap("tab10")
    x_vals = np.arange(n_steps) / steps_per_mm  # convert step indices to mm

    top_lines = []
    bottom_lines = []

    for i, offset in enumerate(offsets):
        color = cmap(i % 10)
        start_cam = random.uniform(*cam_start_range)
        start_lt = random.uniform(*lt_start_range)
        start_llsb = random.uniform(*llsb_start_range)

        cam_path = generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                       x_sorted_cam, bin_edges_cam, devs_cam)
        lt_path = generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                      x_sorted_lt, bin_edges_lt, devs_lt)
        centerline = offset + cam_path + lt_path

        width_error = generate_error_path(start_llsb, n_steps, slope_llsb, intercept_llsb,
                                          x_sorted_llsb, bin_edges_llsb, devs_llsb)
        width = width_error + tow_width_mm

        top_line = centerline + 0.5 * width
        bottom_line = centerline - 0.5 * width

        top_lines.append(top_line)
        bottom_lines.append(bottom_line)

        # --- Plot ---
        if plot == True:
            plt.plot(x_vals, centerline[:n_steps], color=color, label=f"Tow {i + 1} Centerline", linewidth=2)
            plt.plot(x_vals, top_line[:n_steps], linestyle=":", color=color, linewidth=1)
            plt.plot(x_vals, bottom_line[:n_steps], linestyle=":", color=color, linewidth=1)
            plt.plot(x_vals, [offset] * n_steps, linestyle="--", color="gray", alpha=0.6,
                     label="Ideal Centerline" if i == 0 else "")
    if plot == True:
        plt.xlabel("x position [mm]")
        plt.ylabel("y position [mm]")
        plt.title(f"Simulated {num_tows}-Tow Layout with Random Start Errors")
        plt.legend(loc="upper right", ncol=2)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # gaps and overlaps calculation
    # Compute vertical gaps between adjacent tows
    gap_overlap_data = []

    for i in range(num_tows - 1):
        gap_overlap = bottom_lines[i + 1] - top_lines[i]  # vertical space between adjacent tows
        col_name = f"Gap/overlap_Tow{i + 1}_Tow{i + 2}"
        gap_overlap_data.extend(gap_overlap)  # shape

    #gap_overlap_df = pd.DataFrame(gap_overlap_data)
    #print(gap_overlap)
    return gap_overlap_data


# REAL DATA (!deletes a lot of data!, only use as indicator for percentage of gap overlap)

def calculate_real_gap_overlap_percentages(num_tows=5, tow_spacing_mm=6.35):
    offsets = np.linspace(-(num_tows - 1) / 2, (num_tows - 1) / 2, num_tows) * tow_spacing_mm
    top_lines = []
    bottom_lines = []

    for tow in range(2, 2 + num_tows):   #for tow in range(3, 32, 2):
        tow_temp = tow*2-1
        df = get_synced_data(tow_temp, spacesynced=True)

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
    gap_overlap_data = []

    for i in range(num_tows - 1):
        top_i = top_lines[i]
        bottom_next = bottom_lines[i + 1]
        common_len = min(len(top_i), len(bottom_next))

        top_i = top_i[:common_len]
        bottom_next = bottom_next[:common_len]

        gap_overlap = bottom_next - top_i
        gap_overlap_data.extend(gap_overlap)

    #print(gap_overlap)

    return gap_overlap_data

def get_traverse_data():
    real_gap_data = []
    for tow in range(1, 31):
        gap_data = np.array(GAP_exceltoarray()[tow-1])
        real_gap_data.extend(gap_data[:, -2])
        print(tow)

    real_gap_data_cleaned = [x for x in real_gap_data if ~np.isnan(x)]
    return real_gap_data_cleaned

def main():
    # data
    #real_gap_data = calculate_real_gap_overlap_percentages(num_tows=15, tow_spacing_mm=12.5)
    real_gap_data = get_traverse_data()
    mean_real = np.mean(real_gap_data)
    std_real = np.std(real_gap_data)
    print(f'the REAL MEAN = {mean_real}')
    # real_gap_data = filter(lambda x: 4 >= x >= 8, real_gap_data)
    print(real_gap_data)

    gap_overlap_df = generate_multitow_layout(num_tows=200, tow_spacing_mm=12.5, n_steps=2778)
    mean_sim = np.mean(gap_overlap_df)
    std_sim = np.std(gap_overlap_df)
    #print(f'uuhhhuhhh {real_gap_data}')
    #print('wtf')
    print(f'Experimental mean/std = {mean_real}/{std_real}')
    print(f'Model mean/std = {mean_sim}/{std_sim}')

    #plots
    gap_center = 12.5-6.35
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(real_gap_data, label='Experimental', bins=[0]+list(np.linspace(gap_center-1.2, gap_center+1.2, 100+1))+[10], alpha=0.5, density=True)     # bins=[0]+list(np.linspace(6.15-1.2, 6.15+1.2, 80+1))+[10]
    ax.hist(gap_overlap_df, label='Model', bins=[0]+list(np.linspace(gap_center-1.2, gap_center+1.2, 100+1))+[10], alpha=0.5, density=True)
    ax.axvline(mean_real, color='purple', linestyle='-', label='Experimental Mean')
    ax.axvline(mean_sim, color='red', linestyle='-', label='Model Mean')
    ax.set_xlabel("Gap (mm)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.axvline(gap_center, color='black', linestyle='dashed', label='Ideal Gap')
    # plt.title(f"Gaps")
    ax.set_xlim(gap_center-1.2, gap_center+1.2)
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax.legend(fontsize=10)

    plt.xticks(np.linspace(gap_center-1.2, gap_center+1.2, 9))
    #plt.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()


data = main()

# Run the simulation 1000 times
def simulation_verificatoin():
    num_simulations = 250
    gap_percent_list = []
    overlap_percent_list = []
    for i in range(num_simulations):
        print(f"Running simulation {i + 1}/{num_simulations}", end="\r")
        _, _, _, gap_pct, overlap_pct = generate_multitow_layout(num_tows=15, plot=False)
        gap_percent_list.append(gap_pct)
        overlap_percent_list.append(overlap_pct)

    avg_gap = np.mean(gap_percent_list)
    avg_overlap = np.mean(overlap_percent_list)

    print(f"\n\nAfter {num_simulations} simulations of 15-tow layout:")
    print(f"Average Gap Percentage: {avg_gap:.2f}%")
    print(f"Average Overlap Percentage: {avg_overlap:.2f}%")