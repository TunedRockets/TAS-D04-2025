def get_directory_camera_data(camera_tow_number):
    """
    Generates the directory for the camera data files as a function of the tow number
    """
    
    path_start = "Raw data\Data Sans Camera\LLS\Straight lines"
    path_extension = ".mat"
    path_number = "\\" + str(LLS_tow_number) + "\\" + "LLS_" + str(LLS_type) + "_data"
    directory = path_start + path_number + path_extension
    return(directory)