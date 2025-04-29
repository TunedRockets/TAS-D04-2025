import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Handling_ALL_Functions import get_synced_data
from scipy.stats import norm, gamma, skewnorm, logistic, beta, expon, lognorm
import warnings

def best_fit_distribution(data, bins=40, distributions=None):
    y, bin_edges = np.histogram(data, bins=bins, density=True)
    x_mid = (bin_edges[:-1] + bin_edges[1:]) / 2.0
    if distributions is None:
        distributions = [norm, logistic, gamma, beta, expon, lognorm, skewnorm]
    best = {'dist': None, 'params': None, 'sse': np.inf}
    for dist in distributions:
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

def get_all_sensor_data():
    results_LLSA, results_LLSB, results_LT, results_CAM = [], [], [], []
    for i in range(1, 32):
        df = get_synced_data(tow=i, overwrite=False)
        if df.shape[1] > 4:
            df = df.iloc[:, :4]
        elif df.shape[1] == 3:
            df.insert(2, "temp", np.nan)
        df.columns = ["time", "width", "center", "error_LLS_A"]
        results_LLSA.append(df)
    for j in range(1, 32):
        df = get_synced_data(tow=j, overwrite=False)
        df.columns = ["time", "width", "center", "error_LLS_B"]
        results_LLSB.append(df)
    for k in range(1, 32):
        df = get_synced_data(tow=k, overwrite=False)[["time", "error_LT"]]
        results_LT.append(df)
    for w in range(1, 32):
        df = get_synced_data(tow=w, overwrite=False)
        df["error_CAM"] = -df["center"]
        results_CAM.append(df[["time", "error_CAM"]])
    return {
        "LLS_A": pd.concat(results_LLSA, ignore_index=True),
        "LLS_B": pd.concat(results_LLSB, ignore_index=True),
        "LT":    pd.concat(results_LT,   ignore_index=True),
        "CAM":   pd.concat(results_CAM,  ignore_index=True)
    }

def statistical_values(data: pd.DataFrame):
    errors = [
        data['error_LLS_A'],
        data['error_LLS_B'],
        data['error_LT'],
        data['error_CAM']
    ]
    stats = {'mean': [], 'median': [], 'std': [], 'min': [], 'max': []}
    for e in errors:
        stats['mean'].append(round(e.mean(), 4))
        stats['median'].append(round(e.median(), 4))
        stats['std'].append(round(e.std(), 4))
        stats['min'].append(round(e.min(), 4))
        stats['max'].append(round(e.max(), 4))
    return stats

def plot_histograms(data: pd.DataFrame, title: str, bin_widths: list[float] = None):
    distribution_labels = {
        'norm':     'Normal Distribution',
        'logistic': 'Logistic Distribution',
        'gamma':    'Gamma Distribution',
        'beta':     'Beta Distribution',
        'expon':    'Exponential Distribution',
        'lognorm':  'Log-normal Distribution',
        'skewnorm': 'Skew-Normal Distribution'
    }

    fig, ax = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle(title)

    errors = [
        data['width error_LLS_A'],
        data['width error_LLS_B'],
        data['error_LT'],
        data['center_CAM']
    ]
    names = ['error_LLS_A', 'error_LLS_B', 'error_LT', 'error_CAM']
    titles = [
        'Error Tape width before compaction',
        'Error Tape width after compaction',
        'Error robot position',
        'Error tape lateral movement'
    ]
    if bin_widths is None:
        bin_widths = [None] * 4

    for i, vals in enumerate(errors):
        row, col = divmod(i, 2)
        clean = vals.dropna().to_numpy()
        mn, mx = clean.min(), clean.max()
        bw = bin_widths[i]
        bins = 40 if bw is None else np.arange(mn, mx + bw, bw)
        ax[row, col].hist(clean, bins=bins, edgecolor='black', alpha=0.6, density=True)

        best = best_fit_distribution(clean, bins=len(bins) - 1)
        dist, params = best['dist'], best['params']
        friendly = distribution_labels.get(dist.name, dist.name)
        print(f"{names[i]} best fit: {friendly}")

        x = np.linspace(mn, mx, 200)
        pdf = dist.pdf(x, *params[:-2], loc=params[-2], scale=params[-1])
        ax[row, col].plot(x, pdf, '-', lw=2, label=friendly)

        if i == 1:
            ax[row, col].set_xlim(-0.4, 0.2)
        elif i == 2:
            ax[row, col].set_xlim(-1.2, -0.75)
        elif i == 3:
            ax[row, col].set_xlim(-0.5, 1)

        mean_val = clean.mean()
        std_val  = clean.std()

        ax[row, col].axvline(
            mean_val,
            color='red',
            linestyle='-',
            label=f'Mean = {mean_val:.2f}'
        )
        ax[row, col].axvline(
            mean_val + std_val,
            color='orange',
            linestyle='--',
            label=f'+1 Std = {std_val:.2f}'
        )

        ax[row, col].set_title(titles[i])
        ax[row, col].set_xlabel(names[i])
        ax[row, col].set_ylabel('Density')
        ax[row, col].legend()

    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()

def plot_histograms_separated(data: pd.DataFrame, title: str, bin_widths: list[float] = None):
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

    for i, vals in enumerate(errors):
        clean = vals.dropna().to_numpy()
        mn, mx = clean.min(), clean.max()
        bw = bin_widths[i]
        bins = 40 if bw is None else np.arange(mn, mx + bw, bw)

        fig, ax = plt.subplots(figsize=(6, 4))
        fig.suptitle(f"{title} — {titles[i]}")

        ax.hist(clean, bins=bins, edgecolor='black', alpha=0.6, density=True)

        mean_val = clean.mean()
        std_val  = clean.std()

        ax.axvline(
            mean_val,
            linestyle='-',
            color='red',
            label=f'Mean = {mean_val:.2f}'
        )
        ax.axvline(
            mean_val + std_val,
            linestyle='--',
            color='orange',
            label=f'+1 Std = {std_val:.2f}'
        )

        if i in (0, 1, 2, 3):
            ax.set_xlim(-1.2, 1.0)

        ax.set_title(titles[i])
        ax.set_xlabel(names[i])
        ax.set_ylabel('Density')
        ax.legend()
        plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.show()

def main():
    df = pd.concat((get_synced_data(t) for t in range(1, 9)), ignore_index=True)
    df = df[df['width error_LLS_B'] >= -0.4].reset_index(drop=True)

    plot_histograms(
        df,
        title="Sensor Error Histograms (ONLY 9 TOWS)",
        bin_widths=[0.01, 0.01, 0.005, 0.03]
    )
    plot_histograms_separated(
        df,
        title="Sensor Error Histograms (ONLY 9 TOWS)",
        bin_widths=[0.01, 0.01, 0.02, 0.03]
    )

if __name__ == "__main__":
    main()
