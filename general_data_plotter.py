
"""A genera data plotter in order to find how to synchronize later for future steps"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dataclasses import dataclass

import data_handler
import laser_tracker_data_importer

########################################################
def plot_LT(data: pd.DataFrame, name: str):
    time = data["time"]
    x = data["x"]
    y = data["y"]
    z = data["z"]


    v_x, v_y, v_z = [0], [0], [0]
    for i in range(len(time-1)):
        dt = time[i+1] - time[i]

        dx = x[i+1] - x[i]
        x_velocity = dx/dt
        dy = y[i+1] - y[i]
        y_velocity = dy/dt
        dz = z[i + 1] - z[i]
        z_velocity = dz / dt

        v_x.append(x_velocity)
        v_y.append(y_velocity)
        v_z.append(z_velocity)
    # v_x.append(x_velocity)      # this is so the list is the same length as other data
    # v_y.append(y_velocity)
    # v_z.append(z_velocity)


    plt.subplot(231)
    plt.plot(time, x)
    plt.title('LT, x-coordinates')
    plt.xlabel("Time")

    plt.subplot(232)
    plt.plot(time, y)
    plt.title('LT, x-coordinates')
    plt.xlabel("Time")

    plt.subplot(233)
    plt.plot(time, z)
    plt.title('LT, x-coordinates')
    plt.xlabel("Time")

    plt.subplot(234)
    plt.plot(time, v_x)
    plt.title('LT, x-velocities')
    plt.xlabel("Time")

    plt.subplot(235)
    plt.plot(time, v_y)
    plt.title('LT, y-velocities')
    plt.xlabel("Time")

    plt.subplot(236)
    plt.plot(time, v_z)
    plt.title('LT, z-velocities')
    plt.xlabel("Time")

    plt.tight_layout()
    plt.show()






########################################################
def plot_LLS(data: pd.DataFrame, name: str):
    time = data["time"]
    width = data["width"]
    center = data["center"]

    v_width, v_center = [0], [0]
    for i in range(len(time - 1)):
        dt = time[i + 1] - time[i]

        dw = width[i + 1] - width[i]
        x_velocity = dw / dt
        dc = center[i + 1] - center[i]
        y_velocity = dc / dt

        v_width.append(x_velocity)
        v_center.append(y_velocity)

    plt.subplot(121)
    plt.plot(time, width, label='width', color='red')
    plt.plot(time, center, label='center', color='blue')
    plt.legend(loc='upper_right')
    plt.title('LLS, coordinates')
    plt.xlabel("Time")
    plt.ylabel("location")

    plt.subplot(122)
    plt.plot(time, v_width, label='v_width', color='red')
    plt.plot(time, v_center, label='v_center', color='blue')
    plt.legend(loc='upper_right')
    plt.title('LLS, velocities')
    plt.xlabel("Time")
    plt.ylabel("velocity")

    plt.tight_layout()
    plt.show()


#####################################################
def plot_camera(data: pd.DataFrame, name: str):
    time = data["time"]
    width = data["width"]
    center = data["center"]

    v_width, v_center = [0], [0]
    for i in range(len(time - 1)):
        dt = time[i + 1] - time[i]

        dw = width[i + 1] - width[i]
        x_velocity = dw / dt
        dc = center[i + 1] - center[i]
        y_velocity = dc / dt

        v_width.append(x_velocity)
        v_center.append(y_velocity)

    plt.subplot(121)
    plt.plot(time, width, label='width', color='red')
    plt.plot(time, center, label='center', color='blue')
    plt.legend(loc='upper_right')
    plt.title('camera, coordinates')
    plt.xlabel("Time")
    plt.ylabel("location")

    plt.subplot(122)
    plt.plot(time, v_width, label='v_width', color='red')
    plt.plot(time, v_center, label='v_center', color='blue')
    plt.legend(loc='upper_right')
    plt.title('camera, velocities')
    plt.xlabel("Time")
    plt.ylabel("velocity")

    plt.tight_layout()
    plt.show()





######################################################
def main():
    camera_data = pd.read_csv('camera_data.csv')
    plot_camera(camera_data, 'camera')

    LT_data = pd.read_csv('LT_data.csv')
    plot_LT(LT_data, 'Laser Tracker')

    LLS1_data = pd.read_csv('LLS1_data.csv')
    plot_LLS(LLS1_data, 'LLS1')

    LLS2_data = pd.read_csv('LLS2_data.csv')
    plot_LLS(LLS2_data, 'LLS2')