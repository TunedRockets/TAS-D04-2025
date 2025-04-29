import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Handling_ALL_Functions import get_synced_data
from scipy.stats import norm, gamma, skewnorm, logistic, beta, expon, lognorm, skewnorm
import warnings


def best_fit_distribution(data, bins=40, distributions=None):
    y, bin_edges = np.histogram(data, bins=bins, density=True)
    x_mid = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    if distributions is None:
        distributions = [norm, logistic, gamma, beta, expon, lognorm, skewnorm]
    best = {'dist': None, 'params': None, 'sse': np.inf}
    for dist in distributions:
        # skip distributions that can't handle negative values
        if data.min() < 0 and dist in (gamma, beta, expon, lognorm, skewnorm):
            continue
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            try:
                params = dist.fit(data)
                pdf = dist.pdf(x_mid, *params[:-2], loc=params[-2], scale=params[-1])
                sse = np.sum((y - pdf) ** 2)
                if sse < best['sse']:
                    best.update(dist=dist, params=params, sse=sse)
            except Exception:
                continue
    return best


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
        processed_data_LLSA = get_synced_data(tow=i, overwrite=False)

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
        processed_data_LLSB = get_synced_data(tow=j, overwrite=False)
        processed_data_LLSB.columns = ["time", "width", "center", "error_LLS_B"]
        results_LLSB.append(processed_data_LLSB)

    # ---------------------------
    # Process LT sensor data
    # ---------------------------
    for k in range(1, 32):
        processed_data_LT = get_synced_data(tow=k, overwrite=False)
        processed_data_LT = processed_data_LT[["time", "error_LT"]]
        results_LT.append(processed_data_LT)

    # ---------------------------
    # Process CAM sensor data
    # ---------------------------
    for w in range(1, 32):
        processed_data_CAM = get_synced_data(tow=w, overwrite=False)

        # rename camera's "width error" column to "error_CAM"
        processed_data_CAM["error_CAM"] = -processed_data_CAM["center"]
        processed_data_CAM = processed_data_CAM[["time", "error_CAM"]]
        results_CAM.append(processed_data_CAM)

    # Combine into one DataFrame per sensor type
    df_LLSA = pd.concat(results_LLSA, ignore_index=True)
    df_LLSB = pd.concat(results_LLSB, ignore_index=True)
    df_LT = pd.concat(results_LT, ignore_index=True)
    df_CAM = pd.concat(results_CAM, ignore_index=True)

    return {
        "LLS_A": df_LLSA,
        "LLS_B": df_LLSB,
        "LT": df_LT,
        "CAM": df_CAM
    }


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
              data['center_CAM']]

    names = ['error_LLS_A',
             'error_LLS_B',
             'error_LT',
             'error_CAM']

    titles = ['Error Tape width before compaction',
              'Error Tape width after compaction',
              'Error robot position',
              'Error tape lateral movement']
    if bin_widths is None:
        bin_widths = [None] * 4

    for i, vals in enumerate(errors):
        row, col = divmod(i, 2)
        clean = vals.dropna().to_numpy()
        mn, mx = clean.min(), clean.max()
        bw = bin_widths[i]
        bins = 40 if bw is None else np.arange(mn, mx + bw, bw)

        counts, bin_edges, _ = ax[row, col].hist(clean, bins=bins,
                                                 edgecolor='black', alpha=0.6, density=True)

        # fit and plot best distribution
        best = best_fit_distribution(clean, bins=len(bin_edges) - 1)
        dist, params = best['dist'], best['params']
        print(f"{names[i]} best fit: {dist.name}")
        x = np.linspace(mn, mx, 200)
        pdf = dist.pdf(x, *params[:-2], loc=params[-2], scale=params[-1])
        ax[row, col].plot(x, pdf, 'r-', lw=2, label=f'{dist.name} fit')

        # Zoom settings
        if i == 1:
            ax[row, col].set_xlim(-0.4, 0.2)
        elif i == 2:
            ax[row, col].set_xlim(-1.2, -0.75)
        elif i == 3:
            ax[row, col].set_xlim(-0.5, 1)

        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(names[i])
        ax[row, col].set_ylabel('Density')
        mean_val = clean.mean()
        ax[row, col].axvline(mean_val, linestyle='-', label=f'Mean = {mean_val:.2f}')
        ax[row, col].legend()

    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()

def plot_histograms_separated(data: pd.DataFrame,
                    title: str,
                    bin_widths: list[float] = None):
    errors = [
        data['width error_LLS_A'],
        data['width error_LLS_B'],
        data['error_LT'],
        data['center_CAM']
    ]
    names = [
        'width error_LLS_A',
        'width error_LLS_B',
        'error_LT',
        'error_CAM'
    ]
    titles = [
        'Error Tape Width Before Compaction',
        'Error Tape Width After Compaction',
        'Error Robot Position',
        'Error Tape Lateral Movement'
    ]

    
    if bin_widths is None:
        bin_widths = [None] * 4

    figs = []

    for i, vals in enumerate(errors):
        clean = vals.dropna().to_numpy()
        mn, mx = clean.min(), clean.max()
        bw = bin_widths[i]
        bins = 40 if bw is None else np.arange(mn, mx + bw, bw)

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.suptitle(f"{title} — {titles[i]}")

        # histogram
        ax.hist(clean, bins=bins, edgecolor='black', alpha=0.6, density=True)

        ax.axvline(0.0, linestyle='--', color='black', linewidth=1)

        # mean line
        mean_val = clean.mean()
        ax.axvline(mean_val, linestyle='-', color='red',
                   label=f'Mean = {mean_val:.2f}')

        # optional custom x-limits
        if i == 0:
            ax.set_xlim(-1.2, 1.)
        if i == 1:
            ax.set_xlim(-1.2, 1.)
        elif i == 2:
            ax.set_xlim(-1.2, 1.0)
        elif i == 3:
            ax.set_xlim(-1.2, 1.)

        ax.set_title(titles[i])
        ax.set_xlabel(names[i])
        ax.set_ylabel('Density')
        ax.legend()

        fig.tight_layout(rect=[0, 0, 1, 0.95])
        figs.append(fig)
    
    plt.show()


def main():

    # Number of data points in LLS_B to drop
    drop_n = 50 
    dfs=[]

    #TODO: Change this to range(1,30) when possible
    df = pd.concat((get_synced_data(t) for t in range(1, 9)),
                   ignore_index=True)

    #  Drop any data point with LLS_B error < -0.35 (a bit of data manipulation but that's ok)
    df = df[df['width error_LLS_B'] >= -0.4].reset_index(drop=True)

    plot_histograms(
        df,
        title="Sensor Error Histograms (ONLY 9 TOWS)",
        bin_widths=[0.01, 0.01, 0.005, 0.03])

    plot_histograms_separated(df,
                title="Sensor Error Histograms (ONLY 9 TOWS)",
                bin_widths=[0.01, 0.01, 0.02, 0.03])


if __name__ == "__main__":
    main()
