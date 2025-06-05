'''
Some constants that are useful throughout the project, 

authors: Martijn, Johannes

'''


#Dimensions of the set-up
roller_width = 31 #mm
roller_diameter = 40 #mm

# reference coordinates for calculating error
z_ref = -4  # mm

# Reference distances between sensors, positive value is ahead of center point on the tow
TCP_LLS_A = -310.45 #mm
TCP_LLS_B = 107 #mm
TCP_CAM = -roller_diameter * 3.1415926 / 4

# specified tow witdh
tow_width_specified = 6.35 #mm

# programmed y-offset between consecutive tows
y_increment_programmed = 12.5 #mm

font_extra_small = 8
font_small = 12
font_medium = 14
font_large = 16