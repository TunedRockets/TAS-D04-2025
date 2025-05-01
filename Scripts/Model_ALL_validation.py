import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

from Model_ALL_ConsecutiveErrorTheo import consecutive_error, generate_error_path
from Handling_ALL_Functions import get_synced_data

def optimize_num_bins(sensor, test_ratio, bin_range, tow_range, seeds):
    sensor_col_map = {"CAM": 13, "LT": 4, "LLS_A": 10, "LLS_B": 11}
    col = sensor_col_map[sensor]

    mse_results = []

    for num_bins in bin_range:
        total_mse = 0

        for seed in seeds:
            for tow in tow_range:
                data = get_synced_data(tow=tow).to_numpy()
                real = data[:, col]
                start = real[0]
                steps = len(real) - 1

                stats = consecutive_error(
                    sensor=sensor,
                    test_ratio=test_ratio,
                    num_bins=num_bins,
                    bins_show=False,
                    plot_fit=False
                )

                slope, intercept = stats[1], stats[2]
                x_sorted, bin_edges, deviations_per_bin = stats[6], stats[7], stats[8]

                simulated = generate_error_path(
                    start_error=start,
                    n_steps=steps,
                    slope=slope,
                    intercept=intercept,
                    x_sorted=x_sorted,
                    bin_edges=bin_edges,
                    deviations_per_bin=deviations_per_bin,
                    random_seed=seed
                )

                mse = mean_squared_error(real, simulated)
                total_mse += mse

        mse_results.append({"num_bins": num_bins, "total_MSE": total_mse})
        print(f"Bins = {num_bins}, Total MSE = {total_mse:.4f} (over {len(tow_range)} tows x {len(seeds)} seeds)")

    df = pd.DataFrame(mse_results)

    plt.plot(df["num_bins"], df["total_MSE"], marker='o')
    plt.xlabel("Number of Bins")
    plt.ylabel("Total MSE (sum over tows and seeds)")
    plt.title(f"Total MSE vs Bin Count for {sensor}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return df


# Run
if __name__ == "__main__":
    results = optimize_num_bins(
        sensor="CAM",
        test_ratio=0.0001,
        bin_range=range(5, 100),
        tow_range=range(2, 10),
        seeds=[5, 10, 15, 20,30,40,50,60]  # Multiple random seeds
    )

    best = results.loc[results["total_MSE"].idxmin()]
    print(f"\nBest number of bins for CAM: {int(best['num_bins'])} with Total MSE = {best['total_MSE']:.4f}")