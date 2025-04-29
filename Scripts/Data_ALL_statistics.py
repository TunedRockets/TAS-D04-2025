import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Handling_ALL_Functions import get_synced_data
from scipy.stats import norm, gamma, skewnorm

""" Written by Manuel and Diogo, this python imports the processed data from 
    Handling_ALL_Functions and makes the different error plots for the sensors"""

# TODO: Change the code, now the data is synced, the synced_data is a big dataframe.
# TODO: We can probably just call the column with the error directly and plot it.

def get_all_sensor_data():
    results_LLSA = []
    results_LLSB = []
    results_LT = []
    results_CAM = []

    # ---------------------------
    # Process LLS_A sensor data
    # ---------------------------
    for i in range(1, 32):
        processed_data_LLSA = get_processed_data(tow=i, sensor_type="LLS_A", overwrite=False)

        # If there are more than 4 columns, keep only the first 4
        if processed_data_LLSA.shape[1] > 4:
            processed_data_LLSA = processed_data_LLSA.iloc[:, :4]
        # If only 3 columns, insert a placeholder column at index 2 (assuming 'center' is missing)
        elif processed_data_LLSA.shape[1] == 3:
            processed_data_LLSA.insert(2, "temp", np.nan)

        # Rename columns
        processed_data_LLSA.columns = ["time", "width", "center", "error_LLS_A"]
        results_LLSA.append(processed_data_LLSA)

    # ---------------------------
    # Process LLS_B sensor data
    # ---------------------------
    for j in range(1, 32):
        processed_data_LLSB = get_processed_data(tow=j, sensor_type="LLS_B", overwrite=False)
        processed_data_LLSB.columns = ["time", "width", "center", "error_LLS_B"]
        results_LLSB.append(processed_data_LLSB)

    # ---------------------------
    # Process LT sensor data
    # ---------------------------
    for k in range(1, 32):
        processed_data_LT = get_processed_data(tow=k, sensor_type="LT", overwrite=False)
        processed_data_LT = processed_data_LT[["time", "error_LT"]]
        results_LT.append(processed_data_LT)

    # ---------------------------
    # Process CAM sensor data
    # ---------------------------
    for w in range(1, 32):
        processed_data_CAM = get_processed_data(tow=w, sensor_type="CAM", overwrite=False)

        # rename camera's "width error" column to "error_CAM"
        processed_data_CAM["error_CAM"] = -processed_data_CAM["center"] # Added minus sign because camera was inverted
        processed_data_CAM = processed_data_CAM[["time", "error_CAM"]]
        results_CAM.append(processed_data_CAM)

    # Combine into one DataFrame per sensor type
    df_LLSA = pd.concat(results_LLSA, ignore_index=True)
    df_LLSB = pd.concat(results_LLSB, ignore_index=True)
    df_LT   = pd.concat(results_LT, ignore_index=True)
    df_CAM  = pd.concat(results_CAM, ignore_index=True)

    return {
        "LLS_A": df_LLSA,
        "LLS_B": df_LLSB,
        "LT": df_LT,
        "CAM": df_CAM}


def statistical_values(data: pd.DataFrame):
    # Print the column labels of the incoming DataFrame
    print("Input DataFrame columns:", data.columns.tolist())

    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_CAM']]
    mean = []
    median = []
    std = []
    minimum = []
    maximum = []

    for error in errors:
        mean.append(round(error.mean(), 4))
        median.append(round(error.median(), 4))
        std.append(round(error.std(), 4))
        minimum.append(round(error.min(), 4))
        maximum.append(round(error.max(), 4))

    return mean, median, std, minimum, maximum


def plot_histograms(data: pd.DataFrame,
                    title: str,
                    bin_widths: list[float] = None):
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(title)

    errors = [data['width error_LLS_A'], 
              data['width error_LLS_B'], 
              data['error_LT'], 
              data['error_CAM']]
    
    names = ['error_LLS_A', 
             'error_LLS_B', 
             'error_LT', 
             'error_CAM']
    
    titles = ['Error Tape width before compaction',
              'Error Tape width after compaction',
              'Error robot position',
              'Error tape lateral movement']
    if bin_widths is None:
        bin_widths = [None]*4

    for i, vals in enumerate(errors):
        row, col = divmod(i, 2)
        clean = vals.dropna().to_numpy()
        mn, mx = clean.min(), clean.max()
        bw = bin_widths[i]
        bins = 40 if bw is None else np.arange(mn, mx + bw, bw)

        counts, bin_edges, _ = ax[row, col].hist(clean, bins=bins,
                                                edgecolor='black', alpha=0.6, density=True)
        bin_width = bin_edges[1] - bin_edges[0]


        # Zoom settings
        if i == 1:
            ax[row, col].set_xlim(-0.4, 0.2)
        elif i == 2:
            ax[row, col].set_xlim(-1.2, 1.0)
        elif i == 3:
            ax[row, col].set_xlim(-0.75, 1)

        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(names[i])
        ax[row, col].set_ylabel('Density')
        mean_val = clean.mean()
        ax[row, col].axvline(mean_val, linestyle='-', label=f'Mean = {mean_val:.2f}')
        ax[row, col].legend()

    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()


def main():
    
    df = get_synced_data(1)

    plot_histograms(
        df,
        title="Sensor Error Histograms (Tow 1)",
        bin_widths=[0.01, 0.01, 0.02, 0.03]
    )

if __name__ == "__main__":
    main()

