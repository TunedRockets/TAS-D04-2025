
'''
    Way the model works: We input our current error, which we will call x
    A regression model is made by binning the data, calculate the mean of each bin and find a regression line
    we calculate the mean of the next error from the regression model which we call y
    the value of x, the previous error, corresponds to a certain bin which contains a normal curve the randomness in the deviation of y 
    we extract a random point from the normal curve, and we add this value to the before calculated mean
    
    Note: we cant create a value of the mean or the histogram/normal curve of the devation for a certain data point of x(previous error),
    because we don’t have enough data points at that precise point. This is why bins have been created: 
    this works, but will obtain a slight bias, because the deviation normal curve does not 
    correspond to the exact value of x, but only to the values around it
'''
    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.model_selection import train_test_split
from scipy.stats import linregress
def CAM_exceltolist(file_path):
    excel_data = pd.read_excel(file_path, sheet_name=None)
    CAM_sheets_data = []
    for sheet_name, sheet_df in excel_data.items():
        if sheet_name.startswith("Sheet"):
            CAM_sheet_df = sheet_df.iloc[:, 0:]
            CAM_sheets_data.append(CAM_sheet_df)
    return CAM_sheets_data


def load_and_prepare_data(file_path, column_index=4): #CHANGE USED COLUMN
    all_sheets_data = CAM_exceltolist(file_path)  #USE different data loader
    column_arrays = [sheet_df.iloc[:, column_index].dropna().to_numpy() for sheet_df in all_sheets_data]
    combined_array = np.concatenate(column_arrays, axis=0)
    x_values = combined_array[:-1]
    y_values = combined_array[1:]
    return train_test_split(x_values, y_values, test_size=0.5, random_state=42)

def bin_data(x_train, y_train, num_bins):
    sorted_indices = np.argsort(x_train)
    x_sorted = x_train[sorted_indices]
    y_sorted = y_train[sorted_indices]
    bin_edges = np.linspace(0, len(x_sorted), num_bins + 1, dtype=int)
    x_binned = [np.mean(x_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
    y_binned = [np.mean(y_sorted[bin_edges[i]:bin_edges[i + 1]]) for i in range(num_bins)]
    return x_sorted, y_sorted, bin_edges, x_binned, y_binned

def compute_deviations(x_sorted, y_sorted, bin_edges, slope, intercept):
    deviations_per_bin = []
    for i in range(len(bin_edges) - 1):
        bin_start, bin_end = bin_edges[i], bin_edges[i + 1]
        bin_x = x_sorted[bin_start:bin_end]
        bin_y = y_sorted[bin_start:bin_end]
        predicted_y = slope * bin_x + intercept
        deviations = bin_y - predicted_y
        deviations_per_bin.append(deviations)
    return deviations_per_bin

def summarize_bins(x_sorted, y_binned, bin_edges, deviations_per_bin):
    bin_stats = []
    for i in range(len(bin_edges) - 1):
        bin_start = bin_edges[i]
        bin_end = bin_edges[i + 1]
        bin_x_values = x_sorted[bin_start:bin_end]
        y_mean = y_binned[i]
        mu, std = stats.norm.fit(deviations_per_bin[i])
        variance = std**2
        count = bin_end - bin_start
        x_min = np.min(bin_x_values)
        x_max = np.max(bin_x_values)
        x_range_str = f"[{x_min:.2f}, {x_max:.2f}]"
        bin_stats.append({
            "x_range": x_range_str,
            "y_mean": y_mean,
            "deviation_mean": mu,
            "deviation_variance": variance,
            "point_count": count
        })
    return pd.DataFrame(bin_stats)

def predict_next_error(x_value, slope, intercept, x_sorted, bin_edges, deviations_per_bin, confidence):
    y_pred = slope * x_value + intercept
    bin_index = None
    for i in range(len(bin_edges) - 1):
        start_idx = bin_edges[i]
        end_idx = bin_edges[i + 1]
        bin_x_min = x_sorted[start_idx]
        bin_x_max = x_sorted[end_idx - 1]
        if bin_x_min <= x_value <= bin_x_max:
            bin_index = i
            break
    if bin_index is None:
        bin_index = 0 if x_value < x_sorted[0] else len(bin_edges) - 2

    deviations = deviations_per_bin[bin_index]
    deviation_mu, deviation_sigma = stats.norm.fit(deviations)
    adjusted_prediction = y_pred + deviation_mu
    z_score = stats.norm.ppf(1 - (1 - confidence / 100) / 2)
    lower_bound = adjusted_prediction - z_score * deviation_sigma
    upper_bound = adjusted_prediction + z_score * deviation_sigma

    return pd.DataFrame([{"predicted_mean": adjusted_prediction, "lower_bound": lower_bound, "upper_bound": upper_bound, "confidence": confidence,}])

#----------------------------------------------------------
#optional for visualization or something

def plot_regression_with_bins(x_train, y_train, x_binned, y_binned, slope, intercept):
    plt.figure(figsize=(8, 6))
    plt.scatter(x_train, y_train, alpha=0.5, marker='o', edgecolors='k', label="Training Data")
    plt.scatter(x_binned, y_binned, color='red', marker='s', label="Binned Averages")
    plt.plot(x_binned, np.array(x_binned) * slope + intercept, color='red', label='Linear Fit')
    plt.xlabel("X (Train)")
    plt.ylabel("Y (Train)")
    plt.title("Scatter Plot with Equal-Count Binning (Train Data)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_deviation_histograms(x_sorted, bin_edges, deviations_per_bin):
    num_bins = len(deviations_per_bin)
    rows, cols = 5, 8
    fig, axes = plt.subplots(rows, cols, figsize=(20, 10))
    fig.suptitle("Histograms of Deviations per Bin (Training Data)", fontsize=16)
    axes = axes.flatten()
    for i in range(num_bins):
        ax = axes[i]
        bin_devs = deviations_per_bin[i]
        bin_x_values = x_sorted[bin_edges[i]:bin_edges[i + 1]]
        counts, bins, patches = ax.hist(bin_devs, bins=30, edgecolor='black', color='blue', density=True)
        mu, std = stats.norm.fit(bin_devs)
        x_fit = np.linspace(min(bin_devs), max(bin_devs), 100)
        p_fit = stats.norm.pdf(x_fit, mu, std)
        ax.plot(x_fit, p_fit, 'r', linewidth=2)
        x_min = np.min(bin_x_values)
        x_max = np.max(bin_x_values)
        annotation = f"x ∈ [{x_min:.2f}, {x_max:.2f}]\nμ = {mu:.4f}\nσ = {std:.4f}"
        ax.text(0.95, 0.95, annotation, transform=ax.transAxes,
                verticalalignment='top', horizontalalignment='right',
                fontsize=10, bbox=dict(facecolor='white'))
        ax.set_title(f"Bin {i}")
        ax.set_xlabel("Deviation")
        ax.set_ylabel("Density")
        ax.grid(True)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.show()

#------------------------------------------


# -------------------
# Example usage:
# -------------------
#CAM_file_path = r'Data\Data Sans Camera\Camera data\Cameradata_Modified.xlsx'
#x_train, x_test, y_train, y_test = load_and_prepare_data(CAM_file_path)
#x_sorted, y_sorted, bin_edges, x_binned, y_binned = bin_data(x_train, y_train, num_bins=40)
#slope, intercept, *_ = linregress(x_binned, y_binned)
#deviations_per_bin = compute_deviations(x_sorted, y_sorted, bin_edges, slope, intercept)
#bin_stats_df = summarize_bins(x_sorted, y_binned, bin_edges, deviations_per_bin)

#plot_regression_with_bins(x_train, y_train, x_binned, y_binned, slope, intercept)
#plot_deviation_histograms(x_sorted, bin_edges, deviations_per_bin)

#x_input = 0
#prediction_df = predict_next_error(x_input, slope, intercept, x_sorted, bin_edges, deviations_per_bin, 99)
#print("Prediction result:")
#print(prediction_df)

def generate_error_path(start_error, n_steps, slope, intercept, x_sorted, bin_edges, deviations_per_bin, random_seed=0):
    np.random.seed(random_seed)
    error_path = [start_error]
    x_current = start_error

    for _ in range(n_steps):
        # Predict mean of next error
        y_pred = slope * x_current + intercept

        # Find correct bin
        bin_index = None
        for i in range(len(bin_edges) - 1):
            bin_start = bin_edges[i]
            bin_end = bin_edges[i + 1]
            bin_x_min = x_sorted[bin_start]
            bin_x_max = x_sorted[bin_end - 1]
            if bin_x_min <= x_current <= bin_x_max:
                bin_index = i
                break
        # Use edge bin if out of range
        if bin_index is None:
            bin_index = 0 if x_current < x_sorted[0] else len(bin_edges) - 2

        # Get deviation stats and sample a deviation
        deviations = deviations_per_bin[bin_index]
        mu, sigma = stats.norm.fit(deviations)
        sampled_deviation = np.random.normal(mu, sigma) 

        # Next error
        next_error = y_pred + sampled_deviation
        error_path.append(next_error)
        x_current = next_error

    return np.array(error_path)

# === USAGE (after your current setup) ===
n_steps = 1000
start_error = 0

error_path = generate_error_path(
    start_error, n_steps, slope, intercept, x_sorted, bin_edges, deviations_per_bin
)

plt.figure(figsize=(12, 5))
plt.plot(error_path, label="Simulated Error Path")
plt.xlabel("Step")
plt.ylabel("Error")
plt.title("Simulated Machine Error Path Over Time")
plt.grid(True)
plt.legend()
plt.show()
