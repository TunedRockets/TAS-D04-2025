import matplotlib.pyplot as plt
import pandas as pd
import constants
from sklearn.model_selection import train_test_split
from Handling_ALL_Functions import get_synced_data

def plot_variable_relationships(test_ratio=0.5, show=True, save=False, save_path="variable_relationships.png"):
    # Load and concatenate data from all tows
    all_data = []
    for tow_number in range(2, 32):
        df = get_synced_data(tow=tow_number, spacesynced=True)
        all_data.append(df)
    df_all = pd.concat(all_data, ignore_index=True)

    # Select variables of interest
    cols_to_plot = [
        "error_LT", "center_CAM", "width_LLS_A", "width_LLS_B"
    ]

    # Drop NaNs
    df_clean = df_all[cols_to_plot].dropna()

    # Train-test split
    df_train, df_test = train_test_split(df_clean, test_size=test_ratio, random_state=42)

    # Rename for readability
    rename_dict = {
        "error_LT": "LT Error (mm)",
        "center_CAM": "CAM Center (mm)",
        "width_LLS_A": "LLS A Width (mm)",
        "width_LLS_B": "LLS B Width (mm)",
    }
    df_train = df_train.rename(columns=rename_dict)

    # Set up variables and grid
    variables = df_train.columns
    n = len(variables)
    fig, axes = plt.subplots(n, n, figsize=(4.5 * n, 6.5 * n))

    for i in range(n):
        for j in range(n):
            ax = axes[i, j]

            if i == j:
                # Diagonal: histogram
                ax.hist(df_train[variables[i]], bins=30, edgecolor='black', color='skyblue')
                if i == n - 1:
                    ax.set_xlabel(variables[i], fontsize=constants.font_medium)
                else:
                    ax.set_xlabel("")
                    ax.set_xticks([])
                ax.set_ylabel("Frequency", fontsize=constants.font_medium)

            else:
                # Off-diagonal: scatter plot
                ax.scatter(df_train[variables[j]], df_train[variables[i]], alpha=0.6, edgecolors='k', s=10)
                if i == n - 1:
                    ax.set_xlabel(variables[j], fontsize=constants.font_medium)
                else:
                    ax.set_xlabel("")
                    ax.set_xticks([])

                ax.set_ylabel(variables[i], fontsize=constants.font_medium)


    plt.tight_layout(rect=[0, 0.02, 1, 0.95], h_pad=6)

    # Save or show
    if save:
        plt.savefig(save_path, bbox_inches="tight")
    if show:
        plt.show()

if __name__ == "__main__":
    plot_variable_relationships(test_ratio=0.5, show=True, save=False)
