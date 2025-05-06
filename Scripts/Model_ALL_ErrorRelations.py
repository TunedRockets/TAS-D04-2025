
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from Handling_ALL_Functions import get_synced_data


def plot_variable_relationships(test_ratio=0.5, show=True, save=False, save_path="variable_relationships.png"):
    """
    Plot pairwise relationships between key sensor variables across all tows,
    using a train-test split.

    Parameters
    ----------
    test_ratio : float
        Proportion of data to reserve for testing.
    show : bool
        Whether to display the plot interactively.
    save : bool
        Whether to save the plot to disk.
    save_path : str
        Path to save the plot image if save is True.
    """
    # Load and concatenate data from all tows
    all_data = []
    for tow_number in range(1, 32):
        df = get_synced_data(tow=tow_number,spacesynced=True)
        all_data.append(df)
    df_all = pd.concat(all_data, ignore_index=True)

    # Select variables of interest (excluding LLS error columns)
    cols_to_plot = [
        "error_LT", "center_CAM", "width_LLS_A", "width_LLS_B"
    ]

    # Remove rows with NaNs
    df_clean = df_all[cols_to_plot].dropna()

    # Train-test split
    df_train, df_test = train_test_split(df_clean, test_size=test_ratio, random_state=42)

    # Rename for readability
    rename_dict = {
        "error_LT": "LT Error [mm]",
        "center_CAM": "CAM Center [mm]",
        "width_LLS_A": "LLS_A Width [mm]",
        "width_LLS_B": "LLS_B Width [mm]",
    }
    df_train = df_train.rename(columns=rename_dict)

    # Create subplots for pairwise relationships
    variables = df_train.columns
    n = len(variables)
    fig, axes = plt.subplots(n, n, figsize=(4.5 * n, 6.5 * n))  

    for i in range(n):
        for j in range(n):
            ax = axes[i, j]
            if i == j:
                ax.hist(df_train[variables[i]], bins=30, edgecolor='black', color='skyblue')
                ax.set_title(f"Distribution of\n{variables[i]}", fontsize=10)
            else:
                ax.scatter(df_train[variables[j]], df_train[variables[i]], alpha=0.6, edgecolors='k', s=10)
                ax.set_title(f"{variables[i]} vs\n{variables[j]}", fontsize=9)
            if i == n - 1:
                ax.set_xlabel(variables[j], fontsize=9, rotation=45)
            else:
                ax.set_xticks([])
            if j == 0:
                ax.set_ylabel(variables[i], fontsize=9)
            else:
                ax.set_yticks([])

    plt.suptitle(f"Sensor Variable Relationships ", fontsize=20)
    plt.tight_layout(rect=[0, 0.02, 1, 0.95],h_pad=5)  # Adjust bottom margin

    # Save or show
    if save:
        plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()


if __name__ == "__main__":
    plot_variable_relationships(test_ratio=0.5, show=True, save=False)
