import pandas as pd
import numpy as np

# Load the Excel file
file_path = 'Data\Data Sans Camera\LLS\Straight lines\All runs widths\LLS_Width_Before_After.xlsx'  # Replace with your Excel file path

def LLS_exceltoarray(file_path):
    # Read the Excel file into a dictionary where the keys are the sheet names
    # and the values are the dataframes for each sheet.
    excel_data = pd.read_excel(file_path, sheet_name=None)

    # Create an array (list of DataFrames) to store data for each sheet
    LLS_sheets_data = []

    # Iterate through the sheets and store them into the array
    for sheet_name, sheet_df in excel_data.items():
        # If the sheet name matches a specific pattern, for example, starts with "Sheet"
        if sheet_name.startswith("Run"):
            # Drop the first column (assuming the first column is always the first by index)
            LLS_sheet_df = sheet_df.iloc[:, 0:]
            LLS_sheets_data.append(LLS_sheet_df)

    # Now `sheets_data` contains a list of DataFrames for all sheets starting with "Sheet",
    # excluding their first column.
    # You can access each sheet's data by index or iterate over the list.
    # Delete the columns that are not needed in each sheet
    for i, sheet in enumerate(LLS_sheets_data):
        LLS_clean_sheet = np.delete(sheet, [1, 2, 3, 4, 5, 6, 10], axis=1)
        
    # Print the clean sheets
    #    print(f"clean sheet {i + 1}:")
    #    print(clean_sheet)
    

    return LLS_clean_sheet

print(LLS_exceltoarray(file_path))