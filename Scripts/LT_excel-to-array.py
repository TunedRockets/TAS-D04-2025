import pandas as pd

# Load the Excel file
file_path = 'Raw data/Data Sans Camera/Laser tracker/Straight lines/All straight line mats/Excel_Version.xlsx'  # Replace with your Excel file path

# Read the Excel file into a dictionary where the keys are the sheet names
# and the values are the dataframes for each sheet.
excel_data = pd.read_excel(file_path, sheet_name=None)

# Create an array (list of DataFrames) to store data for each sheet
sheets_data = []

# Iterate through the sheets and store them into the array
for sheet_name, sheet_df in excel_data.items():
    # If the sheet name matches a specific pattern, for example, starts with "Sheet"
    if sheet_name.startswith("Sheet"):
        sheets_data.append(sheet_df)

# Now `sheets_data` contains a list of DataFrames for all sheets starting with "Sheet".
# You can access each sheet's data by index or iterate over the list.
# Example: Accessing the first sheet's data
first_sheet_data = sheets_data[0]
print(first_sheet_data)

# If you want to access the data by sheet name
for i, sheet in enumerate(sheets_data):
    print(f"Sheet {i + 1}:")  # Corrected the f-string
    print(sheet)
