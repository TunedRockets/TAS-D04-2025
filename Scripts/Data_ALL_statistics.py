import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Handling_ALL_Functions import get_processed_data

""" Written by Manuel and Diogo, this python imports the processed data from 
    Handling_ALL_Functions and makes the different error plots for the sensors"""

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


        '''if processed_data_LLSB.shape[1] > 4:
            processed_data_LLSB = processed_data_LLSB.iloc[:, :4]
        # If only 3 columns, insert a placeholder at index 1 (assuming 'width' is missing)
        elif processed_data_LLSB.shape[1] == 3:
            processed_data_LLSB.insert(1, "temp", np.nan)'''

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

    errors      = [data['error_LLS_A'], data['error_LLS_B'],
                   data['error_LT'],      data['error_CAM'] ]
    errors_names = ['error_LLS_A', 'error_LLS_B', 'error_LT', 'error_CAM']
    titles      = ['Error Tape width',
                   'Error Tape width after compaction',
                   'Error robot position',
                   'Error tape lateral movement']

    if bin_widths is None:
        bin_widths = [None]*4

    for i, error in enumerate(errors):
        row, col = divmod(i, 2)
        clean = error.dropna().to_numpy()
        mn, mx = clean.min(), clean.max()

        bw = bin_widths[i]
        if bw is None:
            bins = 40
        else:
            bins = np.arange(mn, mx + bw, bw)

        ax[row, col].hist(clean, bins=bins,
                          color='skyblue', edgecolor='black')

        # ** ZOOM IN on i==1 (top right) and i==2 (bottom left) **
        if i == 1:   # top‑right plot (error_LLS_B)
            ax[row, col].set_xlim(-0.5, 0.5)   # example limits
        elif i == 2: # bottom‑left plot (error_LT)
            ax[row, col].set_xlim(-1.5, 1.0)   # example limits
        elif i== 3: # bottom-left plot 
             ax[row, col].set_xlim(-13.0, -12.0)

        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(errors_names[i])
        ax[row, col].set_ylabel('Frequency')

        mean_val = clean.mean()
        ax[row, col].axvline(mean_val, color='red', linestyle='-',
                             label=f'Mean = {mean_val:.2f}')
        ax[row, col].legend()

    plt.tight_layout(rect=[0,0,1,0.96])
    plt.show()

def main():
    # Gather data
    sensor_data = get_all_sensor_data()

    # Create a combined DataFrame of errors
    df_error = pd.concat([
        sensor_data["LLS_A"]["error_LLS_A"].reset_index(drop=True),
        sensor_data["LLS_B"]["error_LLS_B"].reset_index(drop=True),
        sensor_data["LT"]["error_LT"].reset_index(drop=True),
        sensor_data["CAM"]["error_CAM"].reset_index(drop=True)
    ], axis=1)
    df_error.columns = ["error_LLS_A", "error_LLS_B", "error_LT", "error_CAM"]

    # Compute stats
    mean, median, std, minimum, maximum = statistical_values(df_error)


    labels = ["Tape Width Before Compression", 
              "Tape Width After Compression", 
              "Robot Position", 
              "Tape Lateral Movement"]

    for i, label in enumerate(labels):
        print(f"{label}:")
        print(f"  Mean: {mean[i]}")
        print(f"  Median: {median[i]}")
        print(f"  Std Dev: {std[i]}")
        print(f"  Min: {minimum[i]}")
        print(f"  Max: {maximum[i]}")
        print()



    # Plot histograms
    my_bin_widths = [0.005, 0.01, 0.05, 0.02]

    # TODO: Bottom row plots are incorrect, check data 
    # TODO: ('Error robot position', 'Error tape lateral movement')

    plot_histograms(
        df_error,
        title="Sensor Error Histograms",
        bin_widths=my_bin_widths)

if __name__ == '__main__':
    main()
