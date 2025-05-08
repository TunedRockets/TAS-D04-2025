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

        # Conv Feature Map Plot
        plt.figure(figsize=(10, 5))
        for i in range(min(4, conv_maps.shape[0])):
            plt.plot(conv_maps[i], label=f"Filter {i}")
        plt.title("Conv1D Feature Activations")
        plt.xlabel("Step")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    return cosine_score, mse


if __name__ == "__main__":
    score, mse = compare_with_functional_net(tow_number=3, n_steps=300, print_plot=True)
    print(f"Cosine Similarity: {score:.4f}")
    print(f"MSE: {mse:.4f}")