# AFP Defect Prediction Model

Welcome to the AFP (Automated Fiber Placement) Gaps and Overlap Prediction Model. This tool enables simulation of tows during the AFP process and prediction of gaps and overlaps defects based on statistical error modeling.

## 🚀 Getting Started

To launch the model:

1. Open `User_Interface.py` in your Python IDE.
2. Run the script to launch the user interface.

## 📂 Output Files

Any figures saved during execution will be saved to the `Figures` folder.

## ⚙️ Settings Configuration

The following input parameters can be adjusted in the **Settings Section** of the User Interface:

- `num_tows`: Number of adjacent tows to simulate.
- `tow_width`: Width of a single tow.
- `tow_length`: Total length of each tow to be laid.
- `tow_spacing`: Distance between centerlines of adjacent tows.

These parameters directly affect the simulation results and can be used to tune the model for different scenarios.

## 📌 Notes

- Ensure all dependencies are installed (`matplotlib`, `numpy`, etc.).
- Python 3.8+ is recommended.

For any questions or further clarification, refer back to the accompanying scientific article.