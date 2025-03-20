
"""A genera data plotter in order to find how to synchronize later for future steps"""

import matplotlib.pyplot as plt
import pandas as pd

import Handling_ALL_Functions


########################################################
def plot_LT(data: pd.DataFrame, name: str):
    time = data["time"]
    x = data["x"]
    y = data["y"]
    z = data["z"]


    v_x, v_y, v_z = [0], [0], [0]
    for i in range(len(time)-1):
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
    for i in range(len(time) - 1):
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
    for i in range(len(time)-1):
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
    plt.legend(loc='upper right')
    plt.title('camera, coordinates')
    plt.xlabel("Time")
    plt.ylabel("location")

    plt.subplot(122)
    plt.plot(time, v_width, label='v_width', color='red')
    plt.plot(time, v_center, label='v_center', color='blue')
    plt.legend(loc='upper right')
    plt.title('camera, velocities')
    plt.xlabel("Time")
    plt.ylabel("velocity")

    plt.tight_layout()
    plt.show()





######################################################
def main():
    tow_id = 2
    plot_camera(Handling_ALL_Functions.get_processed_data(tow_id,"CAM"), 'camera')

    plot_LT(Handling_ALL_Functions.get_processed_data(tow_id,"LT"), 'Laser Tracker')

    plot_LLS(Handling_ALL_Functions.get_processed_data(tow_id,"LT"), 'Laser Line Scanner 1')

    plot_LLS(Handling_ALL_Functions.get_processed_data(tow_id,"LT"), 'Laser Line Scanner 2')



if __name__ == "__main__":
    main()