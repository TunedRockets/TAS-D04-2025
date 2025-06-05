import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from Model_ALL_Simulation import generate_error_path, consecutive_error
from Handling_ALL_Functions import get_synced_data

# Parameters
tow_number = 3
spacesynced = True
length_tow = 1000  # in mm
n_steps = 360
sampling_rate_sim = n_steps / length_tow  # steps per mm
num_bins = 180

# Load real data
df = get_synced_data(tow=tow_number, spacesynced=spacesynced)
cam = df["center_CAM"].dropna().values
lt = df["error_LT"].dropna().values
x_pos = df["x"].dropna().values
offset_real = cam + lt

# Compute real FFT
real_centerline = offset_real
length_between_points = (x_pos[-1] - x_pos[0]) / len(x_pos)
sampling_rate_real = 1 / length_between_points
fft_real = np.fft.fft(real_centerline)
freq_real = np.fft.fftfreq(len(real_centerline), d=1 / sampling_rate_real)
amp_real = np.abs(fft_real) / len(real_centerline)
mask_real = freq_real > 0
freq_real_pos = freq_real[mask_real]
amp_real_pos = amp_real[mask_real]

# Fit models
bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
    "CAM", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False
)
bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
    "LT", test_ratio=0.5, num_bins=num_bins, bins_show=False, plot_fit=False
)

# Simulate path
start_cam = np.random.uniform(-0.4, 0.6)
start_lt = np.random.uniform(-1.0, -0.8)
cam_path = generate_error_path(start_cam, n_steps, slope_cam, intercept_cam, x_sorted_cam, bin_edges_cam, devs_cam)
lt_path = generate_error_path(start_lt, n_steps, slope_lt, intercept_lt, x_sorted_lt, bin_edges_lt, devs_lt)
simulated_centerline = cam_path + lt_path

# Compute simulated FFT
fft_sim = np.fft.fft(simulated_centerline)
freq_sim = np.fft.fftfreq(len(simulated_centerline), d=1 / sampling_rate_sim)
amp_sim = np.abs(fft_sim) / len(simulated_centerline)
mask_sim = freq_sim > 0
freq_sim_pos = freq_sim[mask_sim]
amp_sim_pos = amp_sim[mask_sim]

# Plot both FFTs
plt.figure(figsize=(10, 5))
plt.plot(freq_real_pos, amp_real_pos, label="Experimental Tow FFT", color='blue')
plt.plot(freq_sim_pos, amp_sim_pos, linestyle="--",label="Simulated Tow FFT", color='orange')
plt.xlabel("Frequency (mm⁻¹)",fontsize=15)
plt.ylabel("Amplitude(mm)",fontsize=15)
plt.xlim(0, 0.2)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
