import pandas as pd
import numpy as np

def LLS_exceltoarray():
    """Read the LLS Excel file into a dictionary where the keys are the sheet names
    and the values are the dataframes for each sheet."""

    excel_data = pd.read_excel('Data\Data Sans Camera\LLS\Straight lines\All runs widths\LLS_Width_Before_After.xlsx', sheet_name=None)

    # Create an array (list of DataFrames) to store data for each sheet
    LLS_clean_sheets_data = []

    # Iterate through the sheets and store them into the array
    for sheet_name, sheet_df in excel_data.items():
        # If the sheet name matches a specific pattern, for example, starts with "Sheet"
        if sheet_name.startswith("Run"):
            # Drop the first column (assuming the first column is always the first by index)
            LLS_sheet_df = sheet_df.iloc[:, 0:]
            LLS_clean_sheet = np.delete(LLS_sheet_df, [1, 2, 3, 4, 5, 6, 10], axis=1)
            LLS_clean_sheets_data.append(LLS_clean_sheet)

    # Now `LLS_clean_sheets_data` contains a list of DataFrames for all sheets starting with "Sheet",
    # excluding the useless columns.
    # You can access each sheet's data by index or iterate over the list.
        
    # Print the clean sheets
    #    print(f"clean sheet {i + 1}:")
    #    print(LLS_clean_sheet)
    

    return LLS_clean_sheets_data
#print(LLS_exceltoarray())