from Model_ALL_ConsecutiveErrorTheo import *
import numpy as np
import matplotlib.pyplot as plt
from Handling_ALL_Functions import get_processed_data
import random
import pandas as pd
import constants 

# Dont use the first function, only use the second one
def generate_exp_vs_sim_layout(tow_width_mm=6.35,
                               n_steps=360,
                               cam_start_range=(-0.6, 0.4),
                               lt_start_range=(-1, -0.8),
                               llsb_start_range=(-0.15, -0.02),
                               experimental_data=None,
                               exp_tow=2,
                               plot=True):

    # --- Load simulation models ---
    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
        "CAM", test_ratio=0.5, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
        "LT", test_ratio=0.5, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_llsb, slope_llsb, intercept_llsb, _, _, _, x_sorted_llsb, bin_edges_llsb, devs_llsb = consecutive_error(
        "LLS_B", test_ratio=0.5, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))

    steps_per_mm = 360 / 1000 
    x_vals = np.arange(n_steps) / steps_per_mm  # convert step indices to mm

    # --- Generate simulated tow ---
    start_cam = random.uniform(*cam_start_range)
    start_lt = random.uniform(*lt_start_range)
    start_llsb = random.uniform(*llsb_start_range)

    cam_path = generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                x_sorted_cam, bin_edges_cam, devs_cam)[:n_steps]
    lt_path = generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                x_sorted_lt, bin_edges_lt, devs_lt)[:n_steps]
    centerline_sim = cam_path + lt_path

    width_error = generate_error_path(start_llsb, n_steps, slope_llsb, intercept_llsb,
                                    x_sorted_llsb, bin_edges_llsb, devs_llsb)[:n_steps]
    width_sim = width_error + tow_width_mm

    top_sim = centerline_sim + 0.5 * width_sim
    bottom_sim = centerline_sim - 0.5 * width_sim

    # --- Plotting ---
    if plot:
        plt.figure(figsize=(12, 8))

        # Simulated tow (color: blue)
        plt.plot(x_vals, centerline_sim, label="Sim Centerline", color="blue", linewidth=2.5)
        plt.plot(x_vals, top_sim, linestyle=":", color="blue", linewidth=1.5)
        plt.plot(x_vals, bottom_sim, linestyle=":", color="blue", linewidth=1.5)

        # Experimental tow (color: orange)
        if experimental_data is not None:
            try:
                exp_cam = experimental_data["center_CAM"].values[:n_steps]
                exp_lt = experimental_data["y"].values[:n_steps]
                exp_lt = exp_lt - 12.5 * (exp_tow - 2) - 125
                exp_center = exp_cam + exp_lt

                exp_width = experimental_data["width_LLS_B"].values[:n_steps]
                exp_top = exp_center + 0.5 * exp_width
                exp_bottom = exp_center - 0.5 * exp_width

                exp_x = experimental_data["x"].values[:n_steps]

                plt.plot(exp_x, exp_center, label="Experimental Centerline", color="orange", linewidth=2.5)
                plt.plot(exp_x, exp_top, linestyle=":", color="orange", linewidth=1.5)
                plt.plot(exp_x, exp_bottom, linestyle=":", color="orange", linewidth=1.5)

            except Exception as e:
                print("Error plotting experimental data:", e)

        plt.xlabel("x position (mm)", fontsize=18)
        plt.ylabel("y position (mm)", fontsize=18)
        plt.title("Simulated Tow vs. Experimental Tow", fontsize=20)
        plt.legend(fontsize=14)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_sim_vs_experimental_tow(tow,
                                  tow_width_mm=6.35,
                                  n_steps=360,
                                  cam_start_range=(-0.6, 0.4),
                                  lt_start_range=(-1, -0.8),
                                  llsb_start_range=(-0.15, -0.02)):
    """
    Plot the geometry of a simulated tow vs. an experimental tow.
    Only the forward pass from x=0 to x=1000 is included for the experimental tow.
    """

    # === Experimental Tow Data ===
    LT_x = get_processed_data(tow, "LT")["x"]
    LT_y = get_processed_data(tow, "LT")["y"]
    LT_time = get_processed_data(tow, "LT")["time"]
    CAM_center = get_processed_data(tow, "CAM")["center"]
    CAM_time = get_processed_data(tow, "CAM")["time"]
    LLS_B_width = get_processed_data(tow, "LLS_B")["width"]
    LLS_B_time = get_processed_data(tow, "LLS_B")["time"]

    # Interpolate CAM and LLS_B onto LT_time
    cam_interp = np.interp(LT_time, CAM_time, CAM_center)
    llsb_interp = np.interp(LT_time, LLS_B_time, LLS_B_width)

    # Convert to NumPy arrays
    LT_x = np.array(LT_x)
    LT_y = np.array(LT_y)
    LT_time = np.array(LT_time)
    cam_interp = np.array(cam_interp)
    llsb_interp = np.array(llsb_interp)

    # Only include values where 0 <= x <= 1000 and stop at first x > 1000
    start_index = next((i for i, x in enumerate(LT_x) if x >= 0), 0)
    end_index = start_index
    while end_index < len(LT_x) and LT_x[end_index] <= 1000:
        end_index += 1

    LT_x = LT_x[start_index:end_index]
    LT_y = LT_y[start_index:end_index]
    cam_interp = cam_interp[start_index:end_index]
    llsb_interp = llsb_interp[start_index:end_index]

    centerline_exp = LT_y + cam_interp - 12.5 * (tow - 2) - 125
    top_edge_exp = centerline_exp + 0.5*llsb_interp
    bottom_edge_exp = centerline_exp - 0.5*llsb_interp

    # === Simulated Tow Data ===
    steps_per_mm = 360 / 1000

    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
        "CAM", test_ratio=0.5, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
        "LT", test_ratio=0.5, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))
    bin_stats_llsb, slope_llsb, intercept_llsb, _, _, _, x_sorted_llsb, bin_edges_llsb, devs_llsb = consecutive_error(
        "LLS_B", test_ratio=0.5, num_bins=180, bins_show=False, plot_fit=False, random_state=random.randint(0, 10000))

    x_vals = np.arange(n_steps) / steps_per_mm  # convert step indices to mm

    start_cam = random.uniform(*cam_start_range)
    start_lt = random.uniform(*lt_start_range)
    start_llsb = random.uniform(*llsb_start_range)

    cam_path = generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                   x_sorted_cam, bin_edges_cam, devs_cam)[:n_steps]
    lt_path = generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                  x_sorted_lt, bin_edges_lt, devs_lt)[:n_steps]
    centerline_sim = cam_path + lt_path

    width_error = generate_error_path(start_llsb, n_steps, slope_llsb, intercept_llsb,
                                      x_sorted_llsb, bin_edges_llsb, devs_llsb)[:n_steps]
    width_sim = width_error + tow_width_mm

    top_sim = centerline_sim + 0.5 * width_sim
    bottom_sim = centerline_sim - 0.5 * width_sim

    # === Plotting ===
    plt.figure(figsize=(12, 8))

    # Simulated tow (orange)
    plt.plot(x_vals, centerline_sim, label="Sim Centerline", color="orange", linewidth=2.5)
    plt.plot(x_vals, top_sim, linestyle=":", color="orange", linewidth=1.5)
    plt.plot(x_vals, bottom_sim, linestyle=":", color="orange", linewidth=1.5)

    # Experimental tow (blue)
    plt.plot(LT_x, centerline_exp, label="Experimental Centerline", color="blue", linewidth=2.5)
    plt.plot(LT_x, top_edge_exp, linestyle=":", color="blue", linewidth=1.5)
    plt.plot(LT_x, bottom_edge_exp, linestyle=":", color="blue", linewidth=1.5)

    plt.xlabel("x position (mm)", fontsize=16)
    plt.ylabel("y position (mm)", fontsize=16)
    plt.title(f"Simulated Tow vs. Experimental Tow {tow}", fontsize=18)
    plt.legend(fontsize=14)
    plt.xticks(np.arange(0, 1100, 100))  # ticks from 0 to 1000 every 100 mm
    plt.grid(True, which='major', axis='x')  # ensure vertical grid is shown
    plt.tight_layout()
    plt.show()

def main():
    exp_tow = 7
    plot_sim_vs_experimental_tow(exp_tow)
    
if __name__ == "__main__":
    main()
