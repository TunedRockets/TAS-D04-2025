import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Define handcrafted convolution filters
def create_handcrafted_filters():
    filters = [
        torch.tensor([[[-1., 0., 1.]]]),   # Upward slope
        torch.tensor([[[1., 0., -1.]]]),   # Downward slope
        torch.tensor([[[1., -2., 1.]]]),   # Peak
        torch.tensor([[[1., 1., 1.]]]),    # Flat
        torch.tensor([[[1., -1., 1.]]])    # Wobble
    ]
    return torch.cat(filters, dim=0)  # shape: (5, 1, 3)

# Step 2: Apply filters and compute activation profile
def compute_pattern_profile(sequence, filters):
    x = torch.tensor(sequence, dtype=torch.float32).unsqueeze(0).unsqueeze(0)  # (1, 1, T)
    activations = F.conv1d(x, filters, padding=1).squeeze(0).detach().abs()    # (5, T)
    pattern_profile = activations.sum(dim=1).numpy()                           # (5,)
    return pattern_profile

# Step 3: Compare two sequences
def compare_sequences(seq1, seq2, plot=False):
    filters = create_handcrafted_filters()
    profile1 = compute_pattern_profile(seq1, filters)
    profile2 = compute_pattern_profile(seq2, filters)
    
    similarity = cosine_similarity([profile1], [profile2])[0][0]

    if plot:
        labels = ["↑ Slope", "↓ Slope", "Peak", "Flat", "Wobble"]
        x = np.arange(len(labels))
        width = 0.35
        plt.bar(x - width/2, profile1, width, label="Seq 1")
        plt.bar(x + width/2, profile2, width, label="Seq 2")
        plt.xticks(x, labels)
        plt.ylabel("Activation Sum")
        plt.title(f"Pattern Profile Comparison\nCosine Similarity = {similarity:.4f}")
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    return similarity

# Step 4: Example use
if __name__ == "__main__":
    # Simulate two sequences
    seq1 = np.concatenate([
        np.linspace(0, 1, 25),
        np.linspace(1, 0.5, 25),
        [0.5, 1.0, 0.5],
        np.ones(22) * 0.6,
        0.1 * np.sin(np.linspace(0, 10*np.pi, 25)) + 0.6
    ])

    seq2 = np.concatenate([
        np.linspace(0, 1, 25),
        np.linspace(1, 0.2, 25),
        [0.2, 1.2, 0.2],
        np.ones(22) * 0.7,
        0.15 * np.sin(np.linspace(0, 10*np.pi, 25)) + 0.6
    ])

    score = compare_sequences(seq1, seq2, plot=True)
    print(f"Pattern similarity score: {score:.4f}")