from mat4py import loadmat

tow_number = 1
path_start = "Raw data\Data Sans Camera\Laser tracker\Straight lines\All straight line mats"
path_extension = ".mat"
path_number = "\\" "TrackerData_" + str(tow_number)
path = path_start + path_number + path_extension
print("the path is: ", path)

data = loadmat(path)
print("The data is: ", data)