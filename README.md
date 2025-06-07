# AFP Defect Prediction Model

Welcome to the AFP (Automated Fiber Placement) Gaps and Overlap Prediction Model. This tool enables simulation of tows during the AFP process and prediction of gap and overlap defects based on statistical error modeling.

## 🚀 Getting Started

To launch the model:

1. Open `User_Interface.py` in your Python IDE.
2. Run the script to launch the user interface.

## 📂 Output Files

Any figures saved during execution will be saved to the `Figures` folder.

## ⚙️ Settings Configuration

The following input parameters can be adjusted in the **Settings Section** of the User Interface:

- `Number of Tows`: Number of adjacent tows to simulate.
- `Tow Width`: Width of a single tow (mm).
- `Tow Length`: Total length of each tow to be laid (mm).
- `Tow Spacing`: Distance between centerlines of adjacent tows (mm).

These parameters directly affect the simulation results and can be used to tune the model for different scenarios.
After changing any of these parameters, make sure to press "Enter" to confirm the change.

## 📌 Notes

- Ensure all dependencies are installed (`matplotlib`, `numpy`, etc.).
- Python 3.8+ is recommended.

For any questions or further clarification, refer back to the accompanying scientific article.