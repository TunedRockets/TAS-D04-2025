from Model_ALL_ConsecutiveErrorTheo import *
import numpy as np
import matplotlib.pyplot as plt
from Handling_ALL_Functions import get_synced_data
import random
import pandas as pd
import constants

steps_per_mm = 360 / 1000  

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

def main():
    exp_tow = 7
    experimental_tow_data = get_synced_data(exp_tow)
    print(experimental_tow_data)
    generate_exp_vs_sim_layout(exp_tow=exp_tow, experimental_data=experimental_tow_data)
    
if __name__ == "__main__":
    main()
