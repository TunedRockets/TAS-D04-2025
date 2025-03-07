import datetime
import threading
import ctypes as ct
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
import pyllt as llt
from pickle import FALSE, TRUE
import sys
import signal
import ipaddress
import csv
import pandas as pd

# Notes
# V6 : Used in the ICCM trials 10 x 1m laydowns
# V6a : Timestamp in callback for more accuracy
# V6b : With failed CSV writer issue

#%% CSV writer approach FAILED
# CSV file creation
# with open('x_df.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
    
# with open('z_df.csv', 'w', newline='') as f1:
#     writer1 = csv.writer(f1)
    
# with open('x1_df.csv', 'w', newline='') as f2:
#         writer3 = csv.writer(f2)
        
# with open('z1_df.csv', 'w', newline='') as f3:
#         writer4 = csv.writer(f3)
        
# with open('zipped.csv', 'w', newline='') as f4:
#         writer5 = csv.writer(f4)
    
#%% Callbck function defnition + initilisation of variables, events

def profile_callback(data, size, user_data):
    global profile_buffer
    global profile_buffer1
    global received
    global received1
    global PCtimestamp
    if user_data == 1: ## data received from sensor 1
        ct.memmove(profile_buffer, data, size)
        # if OfficialRun == 0:
            #print("data reiceved from sensor 1")
        received = 1
        # run = run + 1
        # print (run)
    if user_data == 2:# data received from sensor 2
        ct.memmove(profile_buffer1, data, size)
        # if OfficialRun == 0:
            #print("data reiceved from sensor 2")
        received1 = 1
    if (received and received1): # signal main thread that you received data from both sensors
        event.set()
        received1 = 0
        received = 0
        PCtimestamp = datetime.datetime.now()
        if OfficialRun == 0:
           print("Timestamp in callback loop 1 + 2",PCtimestamp)

#initialize
run = 0
received = 0
received1 = 0

# Parametrize partial profile that only the moment 0 column is transmitted
start_data = 4
data_width = 4
scanner_type = ct.c_int(0)
scanner_type1 = ct.c_int(0)

# Init profile buffer and timestamp info
timestamp = (ct.c_ubyte * 16)()
available_resolutions = (ct.c_uint * 4)()
available_interfaces = (ct.c_uint * 6)()
lost_profiles = ct.c_int()
shutter_opened = ct.c_double(0.0)
shutter_closed = ct.c_double(0.0)
profile_count = ct.c_uint(0)

# Init profile buffer and timestamp info
timestamp1 = (ct.c_ubyte * 16)()
available_resolutions1 = (ct.c_uint * 4)()
available_interfaces1 = (ct.c_uint * 6)()
lost_profiles1 = ct.c_int()
shutter_opened1 = ct.c_double(0.0)
shutter_closed1 = ct.c_double(0.0)
profile_count1 = ct.c_uint(0)

# Callback function
get_profile_cb = llt.buffer_cb_func(profile_callback)
event = threading.Event()

# Null pointer if data not necessary
null_ptr_short = ct.POINTER(ct.c_ushort)()
null_ptr_int = ct.POINTER(ct.c_uint)()

#%% Create instance and set IP address
# hLLT represents sensor 1 
hLLT = llt.create_llt_device(llt.TInterfaceType.INTF_TYPE_ETHERNET)
#hLLT1 represents sensor 2 
hLLT1 = llt.create_llt_device(llt.TInterfaceType.INTF_TYPE_ETHERNET)

# Get available interfaces
ret = llt.get_device_interfaces_fast(hLLT, available_interfaces, len(available_interfaces))
if ret < 1:
    raise ValueError("Error getting interfaces : " + str(ret))

# assign ip adress of sensor 1 to handle representing sensor 1 --> 
# 3232235781 represents an ip adress of 192.168.1.5 which is assigned to sensor 1
# Sid PC ethernet config - LLS A - 2950 - 169.254.175.106 
# KUKA cell PC ethernet config - LLS A - 2950 - XX.XX.XX.XX

#LLS_A_2950_ipaddress = int(ipaddress.ip_address('169.254.175.106')) #Laptop ip
# Trial with 2950-100/BL
# It is now 3060
LLS_A_2950_ipaddress = int(ipaddress.ip_address('169.254.186.181'))

ret = llt.set_device_interface(hLLT, LLS_A_2950_ipaddress, 0)
if ret < 1:
    raise ValueError("Error setting device interface: " + str(ret))
    
# assign ip adress of sensor 2 to handle 2 representing sensor 2 --> 
# 3232235891 represents an ip adress of 192.168.1.115 which is assigned to sensor 2
# Sid PC ethernet config - LLS B 3060 - 169.254.186.181 
# KUKA cell PC ethernet config - LLS A - 2950 - XX.XX.XX.XX

#It is now 3010 (new LLS)
LLS_B_3060_ipaddress = int(ipaddress.ip_address('169.254.158.187')) #Laptop ip
# Trial with 3060-50
#LLS_B_3060_ipaddress = int(ipaddress.ip_address('169.254.165.183'))

ret = llt.set_device_interface(hLLT1, LLS_B_3060_ipaddress, 0)
if ret < 1:
    raise ValueError("Error setting device interface: " + str(ret))

# Connect to sensor 1
ret = llt.connect(hLLT)
print("Connected to hLLT device at IP address: ",str(ipaddress.ip_address(LLS_A_2950_ipaddress)))

if ret < 1:
    raise ConnectionError("Error connect: " + str(ret))


# Connect to sensor 2
ret = llt.connect(hLLT1)
print("Connected to hLLT1 device at IP address: ",str(ipaddress.ip_address(LLS_B_3060_ipaddress)))
if ret < 1:
    raise ConnectionError("Error connect: " + str(ret))

devname = ct.create_string_buffer(256)
vename = ct.create_string_buffer(256)
llt.get_device_name(hLLT, devname, len(devname), vename, len(vename))

devname1 = ct.create_string_buffer(256)
vename1 = ct.create_string_buffer(256)
llt.get_device_name(hLLT1, devname1, len(devname1), vename1, len(vename1))

print("\nDevice name of sensor 1: ",devname.value.decode())
print("Confirm this is LLS A")

print("\nDevice name of sensor 2: ",devname1.value.decode())
print("Confirm this is LLS B")

#%% Set User Modes
# Sensor 1
usermode = 14
ret = llt.read_write_user_mode(hLLT,0,usermode)
if ret < 1:
    raise ValueError("Error setting user mode : " + str(ret))

# Sensor 1
usermode1 = 14
ret = llt.read_write_user_mode(hLLT1,0,usermode1)
if ret < 1:
    raise ValueError("Error setting user mode : " + str(ret))
    
print("\nSensor 1 user mode set to :", usermode)
print("Sensor 2 user mode set to :", usermode1)

#%% Reconnection

# Disconnect
ret = llt.disconnect(hLLT)
if ret < 1:
    raise ConnectionAbortedError("Error while disconnect: " + str(ret))

ret = llt.disconnect(hLLT1)
if ret < 1:
    raise ConnectionAbortedError("Error while disconnect: " + str(ret))

# Connect to sensor 1
ret = llt.connect(hLLT)
if ret < 1:
    raise ConnectionError("Error connect: " + str(ret))

# Connect to sensor 2
ret = llt.connect(hLLT1)
if ret < 1:
    raise ConnectionError("Error connect: " + str(ret))

print("\nDisconnect + Reconnect successful")

#%% Device name
devname = ct.create_string_buffer(256)
vename = ct.create_string_buffer(256)
llt.get_device_name(hLLT, devname, len(devname), vename, len(vename))

devname1 = ct.create_string_buffer(256)
vename1 = ct.create_string_buffer(256)
llt.get_device_name(hLLT1, devname1, len(devname1), vename1, len(vename1))

print("\nDevice name of sensor 1: ",devname.value.decode())
print("LLS A ")

print("\nDevice name of sensor 2: ",devname1.value.decode())
print("LLS B ")

#%% Get, set resolutions

# Get available resolutions of sensor 1
ret = llt.get_resolutions(hLLT, available_resolutions, len(available_resolutions))
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))
# Get available resolutions of sensor 2
ret = llt.get_resolutions(hLLT1, available_resolutions1, len(available_resolutions1))
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))

# Set max. resolution to sensor 1
resolution = available_resolutions[0]
ret = llt.set_resolution(hLLT, resolution)
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))
# Set max. resolution to sensor 2
resolution1 = available_resolutions1[0]
ret = llt.set_resolution(hLLT1, resolution1)
if ret < 1:
    raise ValueError("Error getting resolutions : " + str(ret))
    
print("\nResolution of sensor 1: ",resolution)
print("LLS A ")

print("Resolution of sensor 2: ",resolution1)
print("LLS B ")

#%%

# Declare measuring data arrays
profile_buffer = (ct.c_ubyte*(resolution * data_width))()
x = np.empty(resolution, dtype=float)  # (ct.c_double * resolution)()
z = np.empty(resolution, dtype=float)  # (ct.c_double * resolution)()
x_p = x.ctypes.data_as(ct.POINTER(ct.c_double))
#x_p = (ct.c_double * resolution)()
z_p = z.ctypes.data_as(ct.POINTER(ct.c_double))
intensities = (ct.c_ushort * resolution)()

# Declare measuring data arrays
profile_buffer1 = (ct.c_ubyte*(resolution1 * data_width))()
x1 = np.empty(resolution1, dtype=float)  # (ct.c_double * resolution)()
z1 = np.empty(resolution1, dtype=float)  # (ct.c_double * resolution)()
x_p1 = x1.ctypes.data_as(ct.POINTER(ct.c_double))
#x_p = (ct.c_double * resolution)()
z_p1 = z1.ctypes.data_as(ct.POINTER(ct.c_double))

#%% Make 1 to suspend non essential computations
OfficialRun = 0

#%%  Define arrays and list which will hold data
NoOfProfilesExpected = 5 # 20mS, 3000 profiles per min for 5 mins
Width_XplusZ = resolution*2
Width_X1plusZ1 = resolution1*2

# preallocation
#DataArray = np.zeros((NoOfProfilesExpected,Width_XplusZ))
DataArray1 = np.zeros((NoOfProfilesExpected,Width_X1plusZ1))
#Counter_run_list = np.zeros((NoOfProfilesExpected,Width_XplusZ))
profile_count_list = [None] * NoOfProfilesExpected
profile_count_list1 = [None] * NoOfProfilesExpected
timestamp_list = [None] * NoOfProfilesExpected
shutteropen_list= [None] * NoOfProfilesExpected
shutterclose_list= [None] * NoOfProfilesExpected
shutteropen_list1= [None] * NoOfProfilesExpected
shutterclose_list1= [None] * NoOfProfilesExpected


# Partial profile struct
partial_profile_struct = llt.TPartialProfile(0, start_data, resolution, data_width)
# Partial profile struct
partial_profile_struct1 = llt.TPartialProfile(0, start_data, resolution1, data_width)

#%% Scanner type, partial profile config, trigger set, register callback
# Scanner type
ret = llt.get_llt_type(hLLT, ct.byref(scanner_type))
if ret < 1:
    raise ValueError("Error scanner type: " + str(ret))
# Scanner type
ret = llt.get_llt_type(hLLT1, ct.byref(scanner_type1))
if ret < 1:
    raise ValueError("Error scanner type: " + str(ret))


# Set partial profile as profile config
ret = llt.set_profile_config(hLLT, llt.TProfileConfig.PARTIAL_PROFILE)
if ret < 1:
    raise ValueError("Error setting profile config: " + str(ret))

# Set partial profile as profile config
ret = llt.set_profile_config(hLLT1, llt.TProfileConfig.PARTIAL_PROFILE)
if ret < 1:
    raise ValueError("Error setting profile config: " + str(ret))


# Set trigger
ret = llt.set_feature(hLLT, llt.FEATURE_FUNCTION_TRIGGER, llt.TRIG_INTERNAL)
if ret < 1:
    raise ValueError("Error setting trigger: " + str(ret))

# Set trigger
ret = llt.set_feature(hLLT1, llt.FEATURE_FUNCTION_TRIGGER, llt.TRIG_INTERNAL)
if ret < 1:
    raise ValueError("Error setting trigger: " + str(ret))

# # Set exposure time
# ret = llt.set_feature(hLLT, llt.FEATURE_FUNCTION_EXPOSURE_TIME, 100)
# if ret < 1:
#     raise ValueError("Error setting exposure time: " + str(ret))

# # Set idle time
# ret = llt.set_feature(hLLT, llt.FEATURE_FUNCTION_IDLE_TIME, 3900)
# if ret < 1:
#     raise ValueError("Error idle time: " + str(ret))

# # Set exposure time
# ret = llt.set_feature(hLLT1, llt.FEATURE_FUNCTION_EXPOSURE_TIME, 100)
# if ret < 1:
#     raise ValueError("Error setting exposure time: " + str(ret))

# # Set idle time
# ret = llt.set_feature(hLLT1, llt.FEATURE_FUNCTION_IDLE_TIME, 3900)
# if ret < 1:
#     raise ValueError("Error idle time: " + str(ret))

print("\nExposure and idle time come from user modes \n")


# Set partial profile
ret = llt.set_partial_profile(hLLT, ct.byref(partial_profile_struct))
if ret < 1:
    raise ValueError("Error setting partial profile: " + str(ret))
# Set partial profile
ret = llt.set_partial_profile(hLLT1, ct.byref(partial_profile_struct1))
if ret < 1:
    raise ValueError("Error setting partial profile: " + str(ret))

# Register Callback sensor 1
ret = llt.register_callback(hLLT, llt.TCallbackType.C_DECL, get_profile_cb, 1)
if ret < 1:
    raise ValueError("Error setting callback: " + str(ret))

# Register Callback sensor 2
ret = llt.register_callback(hLLT1, llt.TCallbackType.C_DECL, get_profile_cb, 2)
if ret < 1:
    raise ValueError("Error setting callback: " + str(ret))

#%% Measurement active / Measurement stop

measurement_active = 0
measurement_stopped = 1

print("\nPress Enter to start measurement                   ---1st start")
print("Press CTRL-C to pause measurment")
print("Press x for stopping program")
var = input("")
if var == "":
    # Start transfer
    ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
    if ret < 1:
        raise ValueError("Error starting transfer profiles: " + str(ret))
    ret = llt.transfer_profiles(hLLT1, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
    if ret < 1:
        raise ValueError("Error starting transfer profiles: " + str(ret))
    print("Measurement of both sensors started!")
    measurement_active = 1
    measurement_stopped = 0
else:
    print ("Program exit.")
    # Disconnect
    ret = llt.disconnect(hLLT)
    if ret < 1:
        raise ConnectionAbortedError("Error while disconnect: " + str(ret))

    ret = llt.disconnect(hLLT1)
    if ret < 1:
        raise ConnectionAbortedError("Error while disconnect: " + str(ret))
        
    print("Both sensors disconnected")

    # Delete
    ret = llt.del_device(hLLT)
    if ret < 1:
        raise ConnectionAbortedError("Error while delete: " + str(ret))
    # Delete
    ret = llt.del_device(hLLT1)
    if ret < 1:
        raise ConnectionAbortedError("Error while delete: " + str(ret))
        
    print("Both instances deleted")
    sys.exit(0)

while(measurement_active):

    def signal_handler(sig, frame):
        global measurement_active
        global measurement_stopped
        ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 0)
        # cyclecounter = cyclecounter + 1
        # display(cyclecounter)
        if ret < 1:
            raise ValueError("Error stopping transfer profiles: " + str(ret))
        ret = llt.transfer_profiles(hLLT1, llt.TTransferProfileType.NORMAL_TRANSFER, 0)
        if ret < 1:
            raise ValueError("Error stopping transfer profiles: " + str(ret))
        #measurement_active = 0
        measurement_stopped = 1
        print('Measurement stopped!')
        # Disconnect
        #ret = llt.disconnect(hLLT)
        #if ret < 1:
            #raise ConnectionAbortedError("Error while disconnect: " + str(ret))

        # Delete
        #ret = llt.del_device(hLLT)
        #if ret < 1:
            #raise ConnectionAbortedError("Error while delete: " + str(ret))
        #sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    if (measurement_stopped == 1):
        print("\nPress Enter to restart measurement                 ---2nd | nth start")
        print("Press CTRL-C to pause measurment")
        print("Press x for stopping program")
        # print("Press w to write to disk")
        var = input("")
        if var == "":
            # Start transfer
            ret = llt.transfer_profiles(hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
            if ret < 1:
                raise ValueError("Error starting transfer profiles: " + str(ret))
            ret = llt.transfer_profiles(hLLT1, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
            if ret < 1:
                raise ValueError("Error starting transfer profiles: " + str(ret))
            print("Measurement of both sensors started!")
            measurement_active = 1
            measurement_stopped = 0
        elif var == ("x" or "X"):
            # Disconnect
            ret = llt.disconnect(hLLT)
            if ret < 1:
                raise ConnectionAbortedError("Error while disconnect: " + str(ret))

            ret = llt.disconnect(hLLT1)
            if ret < 1:
                raise ConnectionAbortedError("Error while disconnect: " + str(ret))
                
            print("\nBoth sensors disconnected by x")
            
            # Delete
            ret = llt.del_device(hLLT)
            if ret < 1:
                raise ConnectionAbortedError("Error while delete: " + str(ret))
            # Delete
            ret = llt.del_device(hLLT1)
            if ret < 1:
                raise ConnectionAbortedError("Error while delete: " + str(ret))
                
            print("Both sensor instances deleted by x")
            
            print("Program exit by x")
            sys.exit() 
    
        else:
            print ("Pease press Enter to start the measurement! Start the program again!")
            break

    event.wait()

#%% Evaluate data 
    
    # from sensor 1
    fret = llt.convert_part_profile_2_values(hLLT, profile_buffer, ct.byref(partial_profile_struct), scanner_type, 0, 1,
                                             null_ptr_short, null_ptr_short, null_ptr_short, x_p, z_p, null_ptr_int, null_ptr_int)
    if fret & llt.CONVERT_X == 0 or fret & llt.CONVERT_Z == 0:
        raise ValueError("Error converting data: " + str(ret))
        
    ###Timestamp from sensor 1
    for i in range(16):
        timestamp[i] = profile_buffer[resolution * data_width - 16 + i]

    llt.timestamp_2_time_and_count(timestamp, ct.byref(shutter_opened), ct.byref(shutter_closed), ct.byref(profile_count))

    # from sensor 2
    fret = llt.convert_part_profile_2_values(hLLT1, profile_buffer1, ct.byref(partial_profile_struct1), scanner_type1, 0, 1,
                                            null_ptr_short, null_ptr_short, null_ptr_short, x_p1, z_p1, null_ptr_int, null_ptr_int)
    if fret & llt.CONVERT_X == 0 or fret & llt.CONVERT_Z == 0:
        raise ValueError("Error converting data: " + str(ret))

    ###Timestamp from sensor 2
    for i in range(16):
        timestamp1[i] = profile_buffer1[resolution1 * data_width - 16 + i]

    llt.timestamp_2_time_and_count(timestamp1, ct.byref(shutter_opened1), ct.byref(shutter_closed1), ct.byref(profile_count1))
    

    if OfficialRun == 0:
        
        print("         Run: ",run)
        
        print("X data from sensor A: ", x[500])
        print("X data from sensor B: ", x1[1000])
        
        print("Z data from sensor A: ", z[500])
        print("Z data from sensor B: ", z1[1000])
    
        print("Profile count from sensor A: ", profile_count.value)
        print("Profile count from sensor B: ", profile_count1.value)
        
        print("Profile count from sensor A: ", shutter_opened1.value)
        print("Profile count from sensor B: ", shutter_opened.value)
        
        #full_size = (DataArray.size + DataArray.size + sys.getsizeof(timestamp_list) + sys.getsizeof(profile_count_list) + sys.getsizeof(profile_count_list1) )*1e-06
        #print("Data objects size (GB) : ",full_size*1e-03)
        
        if run == 0:
             PCtimestamp = datetime.datetime.now()
             print("  Run 0 timestamp ", PCtimestamp)
    
    #%% CSV approach FAILED
    
    # x_array = x.reshape(resolution,1)
    # z_array = z.reshape(resolution,1)
    # x1_array = x1.reshape(resolution1,1)
    # z1_array = z1.reshape(resolution1,1)
    
    # x_array_tp = np.transpose(x_array)
    # z_array_tp = np.transpose(z_array)
    # x1_array_tp = np.transpose(x1_array)
    # z1_array_tp = np.transpose(z1_array)
    
    # # Write profile count # and timestamp to list and assemble
    # profile_count_list.insert(run,profile_count.value)
    # profile_count_list1.insert(run,profile_count1.value)
    # timestamp_list.insert(run,PCtimestamp)
    # shutteropen_list.insert(run,shutter_opened.value)
    # shutterclose_list.insert(run,shutter_closed.value)
    # shutteropen_list1.insert(run,shutter_opened1.value)
    # shutterclose_list1.insert(run,shutter_closed1.value)
    # zipped_lists = zip(timestamp_list,profile_count_list,profile_count_list1,shutteropen_list, shutterclose_list, shutteropen_list1, shutterclose_list1)

    # x_df = pd.DataFrame(x_array_tp)
    # z_df = pd.DataFrame(z_array_tp)
    # x1_df = pd.DataFrame(x_array_tp)
    # z1_df = pd.DataFrame(z_array_tp)
    
    # zipped_df = pd.DataFrame(zipped_lists)
    
    # # # Write to pickle try
    # # SensorAProfile = np.hstack((x,z))
    # # SensorBProfile = np.hstack((x1,z1))
    
    # # pickle.dump(SensorAProfile, pickle_file)
    # # pickle.dump(SensorBProfile, pickle_file1)
    
    # #Write CSV try
    # x_df.to_csv('x_df.csv',header=False, mode='a', index=False)
    # z_df.to_csv('z_df.csv',header=False, mode='a', index=False)
    # x1_df.to_csv('x1_df.csv',header=False, mode='a', index=False)
    # z1_df.to_csv('z1_df.csv',header=False, mode='a', index=False)
    # zipped_df.to_csv('zipped.csv',header=False, mode='a', index=False)
    
    #
    # writer.writerow(x_df)
    # writer1.writerow(z_df)
    # writer2.writerow(x1_df)
    # writer3.writerow(z1_df)
    # writer4.writerow(zipped_df)
    
    #PCtimestamp2-PCtimestamp1
    
    
    #%% Original approach Numpy array
    #Reshape to remove empty dimensions, Transpose and Assemble
    #x_array = x.reshape(resolution,1)
    #z_array = z.reshape(resolution,1)
    x1_array = x1.reshape(resolution1,1)
    z1_array = z1.reshape(resolution1,1)
    
    #x_array = np.transpose(x_array)
    #z_array = np.transpose(z_array)
    x1_array = np.transpose(x1_array)
    z1_array = np.transpose(z1_array)
    
    #SensorAProfile = np.hstack((x,z))
    SensorBProfile = np.hstack((x1,z1))
    
    #Write data stack to numpy array
    #DataArray = np.insert(DataArray,run,[SensorAProfile],axis = 0)
    DataArray1 = np.insert(DataArray1,run,[SensorBProfile],axis = 0)
    
    # Write profile count # and timestamp to list and assemble
    profile_count_list.insert(run,profile_count.value)
    profile_count_list1.insert(run,profile_count1.value)
    timestamp_list.insert(run,PCtimestamp)
    shutteropen_list.insert(run,shutter_opened.value)
    shutterclose_list.insert(run,shutter_closed.value)
    shutteropen_list1.insert(run,shutter_opened1.value)
    shutterclose_list1.insert(run,shutter_closed1.value)
    zipped_lists = zip(timestamp_list,profile_count_list,profile_count_list1,shutteropen_list, shutterclose_list, shutteropen_list1, shutterclose_list1)

#%% Time calculation for fps measurement
    if run == 1:
          PCtimestamp1 = datetime.datetime.now()
          print("  1 Run timestamp ", PCtimestamp1)

    if run == 1000:
          PCtimestamp2 = datetime.datetime.now()
          print("  1000 Run timestamp ", PCtimestamp2)
#%% Loop end

    run = run + 1
    
    event.clear()

#%% Memory to disk - Data write (Not run time)
#PCtimestamp2-PCtimestamp1

#df = pd.DataFrame(DataArray)
df1 = pd.DataFrame(DataArray1)
zipped_lists = pd.DataFrame(zipped_lists)

Rundetails = '2000 Shift 1 - Traverse'
#df.to_csv('LLS_A_3060_data.csv',index=False)
df1.to_csv('LLS_B_3010_Traverse_data.csv',index=False)
zipped_lists.to_csv('LLS_A_B_profilenum_timestamp_data.csv',index=False)
print("\nData written to CSV")
with open('readme.txt', 'w') as f:
    f.write(Rundetails)
print("Run details written to text")
# %reset
# print("Run data cleared for next run")

#%% Disconnect and delete

# Disconnect
# ret = llt.disconnect(hLLT)
# if ret < 1:
#     raise ConnectionAbortedError("Error while disconnect: " + str(ret))

ret = llt.disconnect(hLLT1)
if ret < 1:
    raise ConnectionAbortedError("Error while disconnect: " + str(ret))
    
print("Both sensors disconnected")

# # Delete
# ret = llt.del_device(hLLT)
# if ret < 1:
#     raise ConnectionAbortedError("Error while delete: " + str(ret))
# Delete
ret = llt.del_device(hLLT1)
if ret < 1:
    raise ConnectionAbortedError("Error while delete: " + str(ret))
    
print("Both instances deleted")
print("\nThe end")

    
