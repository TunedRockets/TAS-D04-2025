from Model_ALL_ConsecutiveErrorTheo import *
def generate_simulated_tow_centerline(sensor_cam="CAM", sensor_lt="LT", n_steps=300, start_offset=0.0, rdm_seed=0):
    # Get regression + deviation models for CAM and LT
    bin_stats_cam, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
        sensor_cam, test_ratio=0.5, num_bins=100, random_state=42, bins_show=False, plot_fit=False)
    
    bin_stats_lt, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
        sensor_lt, test_ratio=0.5, num_bins=100, random_state=42, bins_show=False, plot_fit=False)

    # Simulate CAM and LT errors
    sim_cam = generate_error_path(start_offset, n_steps, slope_cam, intercept_cam, x_sorted_cam, bin_edges_cam, devs_cam, random_seed=rdm_seed)
    sim_lt = generate_error_path(start_offset, n_steps, slope_lt, intercept_lt, x_sorted_lt, bin_edges_lt, devs_lt, random_seed=rdm_seed)

    # Return the combined offset
    return sim_cam + sim_lt

def generate_multitow_layout(num_tows=5,sensor_LLSB = "LLS B", tow_spacing_mm=6.35, n_steps=300, base_seed=0,start_offset = 0.0,rdm_seed=0):
    bin_stats_LLSB, slope_LLSB, intercept_LLSB, _, _, _, x_sorted_LLSB, bin_edges_LLSB, devs_LLSB = consecutive_error(sensor_LLSB, test_ratio=0.5, num_bins=100, random_state=42, bins_show=False, plot_fit=False)
    width_LLS_B = generate_error_path(start_offset, n_steps, slope_LLSB, intercept_LLSB, x_sorted_LLSB, bin_edges_LLSB, devs_LLSB, random_seed=rdm_seed)+6.35
    Centerline_1 = generate_simulated_tow_centerline(sensor_cam="CAM", sensor_lt="LT", n_steps=300, start_offset=0.0, rdm_seed=0)
    Top_line_1 = Centerline_1+0.5*width_LLS_B
    Bottom_line_1 = Centerline_1-0.5*width_LLS_B