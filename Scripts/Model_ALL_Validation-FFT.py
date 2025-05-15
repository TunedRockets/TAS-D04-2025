import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from mpl_toolkits.mplot3d import Axes3D
from Model_ALL_Simulation import generate_multitow_layout
from Handling_ALL_Functions import get_synced_data
import Model_ALL_Simulation as sim_model

def compute_fft(signal):
    n = len(signal)
    fft_result = np.fft.fft(signal - np.mean(signal))
    freq = np.fft.fftfreq(n)
    magnitude = np.abs(fft_result)[:n // 2]
    freq = freq[:n // 2]
    return freq, magnitude

def find_best_nsteps_and_bins(tow_range=range(2, 16), nsteps_candidates=None, bin_candidates=None):
    if nsteps_candidates is None:
        nsteps_candidates = list(range(100, 400, 5))
    if bin_candidates is None:
        bin_candidates = list(range(30, 180, 5))

    mse_surface = np.zeros((len(bin_candidates), len(nsteps_candidates)))

    for tow in tow_range:
        print(f"Processing Tow {tow}...")
        df = get_synced_data(tow=tow, spacesynced=True)
        cam = df["center_CAM"].dropna().values
        lt = df["error_LT"].dropna().values
        x_pos = df["x"].dropna().values
        min_len = min(len(cam), len(lt), len(x_pos))
        cam = cam[:min_len]
        lt = lt[:min_len]
        x_pos = x_pos[:min_len]
        offset_real = cam + lt
        valid_indices = x_pos <= x_pos[0] + 1000
        offset_real_mm = offset_real[valid_indices]
        freq_real, mag_real = compute_fft(offset_real_mm)

        for b_idx, num_bins in enumerate(bin_candidates):
            bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = sim_model.consecutive_error(
                "CAM", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False)
            bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = sim_model.consecutive_error(
                "LT", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False)

            for s_idx, n_steps in enumerate(nsteps_candidates):
                start_cam = np.random.uniform(-0.4, 0.6)
                start_lt = np.random.uniform(-1.0, -0.8)

                cam_path = sim_model.generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                                         x_sorted_cam, bin_edges_cam, devs_cam)
                lt_path = sim_model.generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                                        x_sorted_lt, bin_edges_lt, devs_lt)
                simulated_centerline = cam_path + lt_path
                freq_sim, mag_sim = compute_fft(simulated_centerline)

                min_len_fft = min(len(mag_real), len(mag_sim))
                mse = mean_squared_error(mag_real[:min_len_fft], mag_sim[:min_len_fft])
                mse_surface[b_idx, s_idx] += mse

    # 3D Plot
    X, Y = np.meshgrid(nsteps_candidates, bin_candidates)
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, mse_surface, cmap='viridis')
    ax.set_xlabel("n_steps")
    ax.set_ylabel("num_bins")
    ax.set_zlabel("Total MSE across all tows")
    ax.set_title("MSE vs. n_steps and num_bins")
    plt.tight_layout()
    plt.show()

    min_mse_idx = np.unravel_index(np.argmin(mse_surface), mse_surface.shape)
    optimal_bins = bin_candidates[min_mse_idx[0]]
    optimal_steps = nsteps_candidates[min_mse_idx[1]]
    print(f"Optimal Configuration -> n_steps: {optimal_steps}, num_bins: {optimal_bins}, MSE: {mse_surface[min_mse_idx]:.4f}")

    return mse_surface, optimal_steps, optimal_bins

def compare_fft_of_paths(n_steps, num_bins, n_tow=3, length_mm=1000):

    offsets = np.linspace(-(n_tow - 1) / 2, (n_tow - 1) / 2, n_tow) * 6.35
    centerline_paths = []

    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = sim_model.consecutive_error(
        "CAM", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False)
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = sim_model.consecutive_error(
        "LT", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False)

    for i, offset in enumerate(offsets):
        start_cam = np.random.uniform(-0.4, 0.6)
        start_lt = np.random.uniform(-1.0, -0.8)

        cam_path = sim_model.generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                                 x_sorted_cam, bin_edges_cam, devs_cam)
        lt_path = sim_model.generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                                x_sorted_lt, bin_edges_lt, devs_lt)

        centerline = offset + cam_path + lt_path
        centerline_paths.append(centerline)

    simulated_centerline = centerline_paths[0]

    df = get_synced_data(tow=2, spacesynced=True)
    cam = df["center_CAM"].dropna().values
    lt = df["error_LT"].dropna().values
    x_pos = df["x"].dropna().values
    min_len = min(len(cam), len(lt), len(x_pos))
    cam = cam[:min_len]
    lt = lt[:min_len]
    x_pos = x_pos[:min_len]

    offset_real = cam + lt
    valid_indices = x_pos <= x_pos[0] + length_mm
    offset_real_mm = offset_real[valid_indices]

    freq_real, mag_real = compute_fft(offset_real_mm)
    freq_sim, mag_sim = compute_fft(simulated_centerline)

    plt.figure(figsize=(12, 6))
    plt.plot(freq_real, mag_real, label="Experimental Path FFT", color='red')
    plt.plot(freq_sim, mag_sim, label="Simulated Path FFT", color='blue', linestyle='--')
    plt.xlabel("Frequency(Hz)")
    plt.ylabel("Amplitude")
    plt.title(f"Frequency Domain Comparison of Offset Paths (Tow {n_tow}) over {length_mm} mm")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    tows_to_plot = [3, 6, 10, 18]  # Tow numbers for comparison
    n_steps = 240
    num_bins = 140
    length_mm = 1000

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))  # 2x2 subplot grid
    axes = axes.flatten()  # For easy iteration

    for i, tow in enumerate(tows_to_plot):
        # Experimental Data
        df = get_synced_data(tow=tow, spacesynced=True)
        cam = df["center_CAM"].dropna().values
        lt = df["error_LT"].dropna().values
        x_pos = df["x"].dropna().values
        min_len = min(len(cam), len(lt), len(x_pos))
        cam = cam[:min_len]
        lt = lt[:min_len]
        x_pos = x_pos[:min_len]
        offset_real = cam + lt
        valid_indices = x_pos <= x_pos[0] + length_mm
        offset_real_mm = offset_real[valid_indices]

        # FFT of experimental path
        freq_real, mag_real = compute_fft(offset_real_mm)

        # Simulated path
        bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = sim_model.consecutive_error(
            "CAM", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False)
        bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = sim_model.consecutive_error(
            "LT", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False)

        start_cam = np.random.uniform(-0.4, 0.6)
        start_lt = np.random.uniform(-1.0, -0.8)

        cam_path = sim_model.generate_error_path(start_cam, n_steps, slope_cam, intercept_cam,
                                                 x_sorted_cam, bin_edges_cam, devs_cam)
        lt_path = sim_model.generate_error_path(start_lt, n_steps, slope_lt, intercept_lt,
                                                x_sorted_lt, bin_edges_lt, devs_lt)

        simulated_centerline = cam_path + lt_path
        freq_sim, mag_sim = compute_fft(simulated_centerline)

        # Plot FFT comparison
        ax = axes[i]
        ax.plot(freq_real, mag_real, label=f"Tow {tow} Real", color='red')
        ax.plot(freq_sim, mag_sim, label="Simulation", color='blue', linestyle='--')
        ax.set_title(f"Tow {tow}",fontsize=18)
        ax.set_xlabel("Frequency (Hz)",fontsize=14)
        ax.set_ylabel("Amplitude",fontsize=14)
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.suptitle("FFT Comparison of 4 Tows and 4 Simulations", fontsize=16, y=1.02)
    plt.show()

#from 3 different runs optimum values
#n_steps: 265, num_bins: 140, MSE: 27.5274
#n_steps: 235, num_bins: 150, MSE: 26.1452
#n_steps: 240, num_bins: 140, MSE: 25.2865
