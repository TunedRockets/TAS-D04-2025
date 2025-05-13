import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from Handling_ALL_Functions import get_synced_data
from Model_ALL_ConsecutiveErrorTheo import consecutive_error, generate_error_path

# Step 1: Define handcrafted filters
def create_handcrafted_filters():
    filters = [
        torch.tensor([[[-1., 0., 1.]]]),           # Upward slope
        torch.tensor([[[1., 0., -1.]]]),           # Downward slope
        torch.tensor([[[1., -2., 1.]]]),           # Peak
        torch.tensor([[[-1., 2., -1.]]]),          # Trough
        torch.tensor([[[0., 0., 0.]]]),            # Placeholder for flat (will override)
        torch.tensor([[[1., -1., 1.]]]),           # Wobble
        torch.tensor([[[1., -2., 2., -1.]]]),      # Wiggle Up-Down-Up
        torch.tensor([[[-1., 2., -2., 1.]]]),      # Wiggle Down-Up-Down
        torch.tensor([[[1., 0., 0., 0., -1.]]]),   # Long slope
        torch.tensor([[[1., -4., 6., -4., 1.]]])   # Sharp spike
    ]
    max_len = max(f.shape[-1] for f in filters)
    padded = [F.pad(f, (0, max_len - f.shape[-1])) for f in filters]
    return torch.cat(padded, dim=0)

# Step 2: Convolve with filters
def compute_pattern_profile(sequence, filters):
    x = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # (1, 1, T)
    activations = F.conv1d(x, filters, padding=filters.shape[-1] // 2).squeeze(0).detach().abs()
    
    dx = F.conv1d(x, torch.tensor([[[-1., 0., 1.]]]), padding=1).squeeze().abs()
    flatness_score = (dx < 0.005).float().sum().item()

    profile = activations.sum(dim=1).numpy()
    profile[4] = flatness_score  # override 'Flat' entry
    return profile

# Step 3: Compare profiles
def compare_sequences(seq1, seq2, plot=False):
    filters = create_handcrafted_filters()
    profile1 = compute_pattern_profile(seq1, filters)
    profile2 = compute_pattern_profile(seq2, filters)
    similarity = cosine_similarity([profile1], [profile2])[0][0]

    if plot:
        labels = [
            "↑ Slope", "↓ Slope", "Peak", "Trough", "Flat", "Wobble",
            "Wiggle ↑↓↑", "Wiggle ↓↑↓", "Long Slope", "Spike"
        ]
        x = np.arange(len(labels))
        width = 0.35
        plt.figure(figsize=(12, 5))
        plt.bar(x - width/2, profile1, width, label="Real Tow")
        plt.bar(x + width/2, profile2, width, label="Simulated Tow")
        plt.xticks(x, labels, rotation=45)
        plt.ylabel("Activation Sum")
        plt.title(f"Pattern Profile Comparison\nCosine Similarity = {similarity:.4f}")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return similarity

# Step 4: Get real and simulated centerlines and compare
def compare_real_vs_simulated_pattern(tow_number=3, n_steps=300, random_seed=10, plot=True):
    data_real = get_synced_data(tow=tow_number, spacesynced=True)
    real_cam = data_real["center_CAM"].values[:n_steps + 1]
    real_lt = data_real["error_LT"].values[:n_steps + 1]
    real_centerline = real_cam + real_lt

    _, slope_cam, intercept_cam, _, _, _, x_sorted_cam, bin_edges_cam, devs_cam = consecutive_error("CAM", 0.5, 100)
    _, slope_lt, intercept_lt, _, _, _, x_sorted_lt, bin_edges_lt, devs_lt = consecutive_error("LT", 0.5, 100)

    sim_cam = generate_error_path(real_cam[0], n_steps, slope_cam, intercept_cam, x_sorted_cam, bin_edges_cam, devs_cam, random_seed)
    sim_lt = generate_error_path(real_lt[0], n_steps, slope_lt, intercept_lt, x_sorted_lt, bin_edges_lt, devs_lt, random_seed)
    sim_centerline = sim_cam + sim_lt

    return compare_sequences(real_centerline, sim_centerline, plot=plot)

# Run it
if __name__ == "__main__":
    score = compare_real_vs_simulated_pattern(tow_number=3, n_steps=300, random_seed=42, plot=True)
    print(f"Pattern similarity score: {score:.4f}")
