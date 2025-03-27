import pandas as pd

# Load the Excel file
CAM_file_path = 'Data\Data Sans Camera\Camera data\Cameradata_Modified.xlsx'  # Replace with your Excel file path

def CAM_exceltolist():
    # Read the Excel file into a dictionary where the keys are the sheet names
    # and the values are the dataframes for each sheet.
    excel_data = pd.read_excel(CAM_file_path, sheet_name=None)

    # Create an array (list of DataFrames) to store data for each sheet
    CAM_sheets_data = []

    # Iterate through the sheets and store them into the array
    for sheet_name, sheet_df in excel_data.items():
        # If the sheet name matches a specific pattern, for example, starts with "Sheet"
        if sheet_name.startswith("Sheet"):
            # Drop the first column (assuming the first column is always the first by index)
            CAM_sheet_df = sheet_df.iloc[:, 0:]
            CAM_sheets_data.append(CAM_sheet_df)

    # Now `CAM_sheets_data` contains a list of DataFrames for all sheets starting with "Sheet",
    # excluding the useless columns.
    # You can access each sheet's data by index or iterate over the list.

    # Print the sheets without the first column
    #for i, sheet in enumerate(sheets_data):
    #    print(f"Sheet {i + 1}:")
    #    print(LT_sheet_df)

    return CAM_sheets_data
#print(CAM_exceltolist())
