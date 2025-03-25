import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Handling_ALL_Functions import get_processed_data

def get_all_sensor_data():
    results_LLSA = []
    results_LLSB = []
    results_LT = []
    results_CAM = []

    # Process LLS_A sensor data
    for i in range(1, 32):  # Iterate from 1 to 31
        processed_data_LLSA = get_processed_data(tow=i, sensor_type="LLS_A", overwrite=False)
        # If there are more than 4 columns, keep only the first 4.
        if processed_data_LLSA.shape[1] > 4:
            processed_data_LLSA = processed_data_LLSA.iloc[:, :4]
        # If only 3 columns, insert a column for "center" at index 2.
        elif processed_data_LLSA.shape[1] == 3:
            processed_data_LLSA.insert(2, "temp", np.nan)
        processed_data_LLSA.columns = ["time", "width", "center", "error_LLS_A"]
        results_LLSA.append(processed_data_LLSA)

    # Process LLS_B sensor data
    for j in range(1, 32):
        processed_data_LLSB = get_processed_data(tow=j, sensor_type="LLS_B", overwrite=False)
        if processed_data_LLSB.shape[1] > 4:
            processed_data_LLSB = processed_data_LLSB.iloc[:, :4]
        elif processed_data_LLSB.shape[1] == 3:
            processed_data_LLSB.insert(2, "temp", np.nan)
        processed_data_LLSB.columns = ["time", "width", "center", "error_LLS_B"]
        results_LLSB.append(processed_data_LLSB)

    # Process LT sensor data
    for k in range(1, 32):
        processed_data_LT = get_processed_data(tow=k, sensor_type="LT", overwrite=False)
        if processed_data_LT.shape[1] > 4:
            processed_data_LT = processed_data_LT.iloc[:, :4]
        elif processed_data_LT.shape[1] == 3:
            processed_data_LT.insert(2, "temp", np.nan)
        processed_data_LT.columns = ["time", "width", "center", "error_LT"]
        results_LT.append(processed_data_LT)

    # Process CAM sensor data
    for w in range(1, 32):
        processed_data_CAM = get_processed_data(tow=w, sensor_type="CAM", overwrite=False)
        if processed_data_CAM.shape[1] > 4:
            processed_data_CAM = processed_data_CAM.iloc[:, :4]
        elif processed_data_CAM.shape[1] == 3:
            processed_data_CAM.insert(2, "temp", np.nan)
        processed_data_CAM.columns = ["time", "width", "center", "error_CAM"]
        results_CAM.append(processed_data_CAM)

    # Combine the lists of DataFrames into one DataFrame per sensor type
    df_LLSA = pd.concat(results_LLSA, ignore_index=True)
    df_LLSB = pd.concat(results_LLSB, ignore_index=True)
    df_LT   = pd.concat(results_LT, ignore_index=True)
    df_CAM  = pd.concat(results_CAM, ignore_index=True)

    return {
        "LLS_A": df_LLSA,
        "LLS_B": df_LLSB,
        "LT": df_LT,
        "CAM": df_CAM
    }

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

def plot_histograms(data: pd.DataFrame, title: str):
    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(title)

    errors = [data['error_LLS_A'], data['error_LLS_B'], data['error_LT'], data['error_CAM']]
    errors_names = ['error_LLS_A', 'error_LLS_B', 'error_LT', 'error_CAM']
    titles = ['Error LLS A vs. time',
              'Error LLS B vs. time',
              'Error Laser Tracker vs. time',
              'Error Camera vs. time']

    for i, error in enumerate(errors):
        row = i // 2
        col = i % 2
        ax[row, col].hist(error, bins=20, color='skyblue', edgecolor='black')
        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(errors_names[i])
        ax[row, col].set_ylabel('Frequency')

def main():
    # Get all sensor data (from tow 1 to 31)
    sensor_data = get_all_sensor_data()

    # Create a combined DataFrame from the error columns
    df_error = pd.concat([
        sensor_data["LLS_A"]["error_LLS_A"].reset_index(drop=True),
        sensor_data["LLS_B"]["error_LLS_B"].reset_index(drop=True),
        sensor_data["LT"]["error_LT"].reset_index(drop=True),
        sensor_data["CAM"]["error_CAM"].reset_index(drop=True)
    ], axis=1)
    df_error.columns = ["error_LLS_A", "error_LLS_B", "error_LT", "error_CAM"]

    # Calculate and print statistical values
    mean, median, std, minimum, maximum = statistical_values(df_error)
    print("Mean:", mean)
    print("Median:", median)
    print("Standard Deviation:", std)
    print("Min:", minimum)
    print("Max:", maximum)

    # Plot histograms for the error values
    plot_histograms(df_error, "Sensor Error Histograms")
    plt.show()

if __name__ == '__main__':
    main()
