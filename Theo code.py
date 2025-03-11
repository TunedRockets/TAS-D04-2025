import numpy as np

# Load the CSV, skipping the header row
data = np.loadtxt(
    "Raw data/Data Sans Camera/Laser tracker/Straight lines/1/1.csv",
    delimiter=",",
    skiprows=1
)

# Extract columns 2, 3, 4, and 13 (zero-based: 1, 2, 3, 12)
x_arr = data[:, 1]
y_arr = data[:, 2]
z_arr = data[:, 3]
time_arr = data[:, 12]

print("x_arr:", x_arr)
print("y_arr:", y_arr)
print("z_arr:", z_arr)
print("time_arr:", time_arr)
