" Nothing here yet but bro is cooking "

import pandas as pd

# Load the Excel file
file_path = 'Data/Data Sans Camera/Laser tracker/Straight lines/All straight line mats/Excel_Version.xlsx'  # Replace with your Excel file path

def LT_exceltoarray(file_path):
    # Read the Excel file into a dictionary where the keys are the sheet names
    # and the values are the dataframes for each sheet.
    excel_data = pd.read_excel(file_path, sheet_name=None)

    # Create an array (list of DataFrames) to store data for each sheet
    sheets_data = []

    # Iterate through the sheets and store them into the array
    for sheet_name, sheet_df in excel_data.items():
        # If the sheet name matches a specific pattern, for example, starts with "Sheet"
        if sheet_name.startswith("Sheet"):
            # Drop the first column (assuming the first column is always the first by index)
            sheet_df = sheet_df.iloc[:, 0:]
            sheets_data.append(sheet_df)

    # Now `sheets_data` contains a list of DataFrames for all sheets starting with "Sheet",
    # excluding their first column.
    # You can access each sheet's data by index or iterate over the list.

    # Print the sheets without the first column
    #for i, sheet in enumerate(sheets_data):
    #    print(f"Sheet {i + 1}:")
    #    print(sheet)

    return sheets_data

print(LT_exceltoarray(file_path))

