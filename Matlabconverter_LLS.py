import scipy.io
import numpy as np
import glob
import os

def mat_to_txt(directory, file_pattern="Run*Indices.mat", delimiter=","):
    """
    Converts MATLAB .mat files to text (.txt) files for use in Python.

    Parameters:
    - directory (str): Path to the folder containing .mat files.
    - file_pattern (str): Wildcard pattern for .mat files (e.g., 'Run*Indices.mat').
    - delimiter (str): Delimiter for text file (default: ',').
    """
    directory = os.path.abspath(directory)
    search_path = os.path.join(directory, file_pattern)
    files = glob.glob(search_path)

    if not files:
        print(f"No .mat files found in: {directory}")
        return

    for file in files:
        print(f"Processing: {file}")
        mat_data = scipy.io.loadmat(file)

        # Filter out MATLAB metadata fields
        mat_data = {k: v for k, v in mat_data.items() if not k.startswith("__")}

        for key, value in mat_data.items():
            if isinstance(value, np.ndarray) and np.issubdtype(value.dtype, np.number):
                output_file = os.path.join(directory, f"{os.path.basename(file).replace('.mat', '')}_{key}.txt")

                # Save as text file
                np.savetxt(output_file, value, delimiter=delimiter, fmt="%.6f")
                print(f"✅ Saved {output_file}")

# Example usage
directory = r"C:/Users/srott/PycharmProjects/TAS-D04-2025/Raw data/Data Sans Camera/LLS/Straight lines/All Runs LLS mats/Converttest"
mat_to_txt(directory, file_pattern="Run*Indices.mat", delimiter=",")
