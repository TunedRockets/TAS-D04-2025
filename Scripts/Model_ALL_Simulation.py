import torch
import torch.nn.functional as F
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

from Model_ALL_ConsecutiveErrorTheo import consecutive_error, generate_error_path
from Handling_ALL_Functions import get_synced_data

def compare_with_functional_net(tow_number=3, n_steps=300, print_plot=False):
    # Load models
    _, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error(
        "CAM", test_ratio=0.5, num_bins=100)
    _, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error(
        "LT", test_ratio=0.5, num_bins=100)

    # Real path
    data_real = get_synced_data(tow=tow_number, spacesynced=True)
    real_cam = data_real["center_CAM"].values[:n_steps + 1]
    real_lt = data_real["error_LT"].values[:n_steps + 1]
    real_centerline = real_cam + real_lt

    # Simulated path
    start_cam = real_cam[0]
    start_lt = real_lt[0]
    sim_cam = generate_error_path(start_cam, n_steps, slope_cam, intercept_cam, x_sorted_cam, bin_edges_cam, devs_cam)
    sim_lt = generate_error_path(start_lt, n_steps, slope_lt, intercept_lt, x_sorted_lt, bin_edges_lt, devs_lt)
    sim_centerline = sim_cam + sim_lt

    # Inject synthetic wave (optional)
    sim_centerline_wave = sim_centerline + 0.2 * np.sin(np.linspace(0, 4 * np.pi, len(sim_centerline)))

    # Convert to tensors
    real_tensor = torch.tensor(real_centerline, dtype=torch.float32).unsqueeze(0).unsqueeze(2)
    sim_tensor = torch.tensor(sim_centerline, dtype=torch.float32).unsqueeze(0).unsqueeze(2)
    sim_wave_tensor = torch.tensor(sim_centerline_wave, dtype=torch.float32).unsqueeze(0).unsqueeze(2)

    # Functional model setup
    conv_weight = nn.Parameter(torch.randn(16, 1, 5))
    conv_bias = nn.Parameter(torch.zeros(16))
    lstm = nn.LSTM(input_size=16, hidden_size=64, batch_first=True)
    fc_weight = nn.Parameter(torch.randn(32, 64))
    fc_bias = nn.Parameter(torch.zeros(32))

    def encode_path(x):
        x = x.transpose(1, 2)
        x = F.conv1d(x, conv_weight, conv_bias, padding=2)
        conv_activations = x.clone().detach()
        x = F.relu(x)
        x = x.transpose(1, 2)
        lstm_out, (h_n, _) = lstm(x)
        embedding = F.linear(h_n[-1], fc_weight, fc_bias)
        return F.normalize(embedding, p=2, dim=1), conv_activations

    # Run forward
    real_tensor.requires_grad_()
    real_emb, real_activ = encode_path(real_tensor)
    sim_emb, _ = encode_path(sim_tensor)
    sim_wave_emb, _ = encode_path(sim_wave_tensor)

    cosine_score = F.cosine_similarity(real_emb, sim_emb).item()
    cosine_score_wave = F.cosine_similarity(real_emb, sim_wave_emb).item()
    mse = F.mse_loss(real_tensor.squeeze(), sim_tensor.squeeze()).item()

    # Saliency
    similarity = F.cosine_similarity(real_emb, sim_emb)
    similarity.backward()
    saliency = real_tensor.grad.abs().squeeze().detach().numpy()

    # Conv activations (first 4)
    conv_maps = real_activ.squeeze().cpu().numpy()  # (channels, time)

    # Plots
    if print_plot:
        fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)

        axs[0].plot(real_centerline, label="Real", color='red')
        axs[0].plot(sim_centerline, label="Simulated", color='blue')
        axs[0].set_title(f"CosSim: {cosine_score:.4f} | CosSim w/ Wave: {cosine_score_wave:.4f} | MSE: {mse:.4f}")
        axs[0].legend()
        axs[0].grid(True)

        axs[1].plot(np.abs(real_centerline - sim_centerline), color='purple')
        axs[1].set_title("Absolute Difference")
        axs[1].grid(True)

        axs[2].plot(real_centerline - sim_centerline, color='orange')
        axs[2].set_title("Signed Difference")
        axs[2].grid(True)

        axs[3].plot(saliency, color='black')
        axs[3].set_title("Saliency Map (Influence of Step on Similarity)")
        axs[3].grid(True)

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

gap_overlap_df, gap_df, overlap_df, gap_percent, overlap_percent = generate_multitow_layout(num_tows=1)

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

def main():

    real_gap_df, real_gap_pct, real_overlap_pct = calculate_real_gap_overlap_percentages(num_tows=30)
    
if __name__ == "__main__":
    main()
