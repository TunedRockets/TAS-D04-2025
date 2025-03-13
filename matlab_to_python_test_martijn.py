import scipy.io

path_start = "Raw data\Data Sans Camera\LLS\Straight lines"
path_extension = ".csv"
path_number = "\\" + str(line_id) + "\\" + "LLS_A_B_profilenum_timestamp_data"
path = path_start + path_number + path_extension
mat = scipy.io.loadmat(path)