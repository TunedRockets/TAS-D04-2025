import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

#@dataclass
#class Model_Regression:
#    bin_error: list     # this is the location of the bin: E_i
#    mean:list           # this is the mean value of the bin: E_i+1
#    variance: list      # this is the variance of the bin: sigma^2?


def fit(bin_error: np.array, bin_mean: np.array, bin_variance: np.array):
    # mean
    mu_a, mu_b, mu_c = get_regression(bin_error, bin_mean)
    plot_function(mu_a, mu_b, mu_c, bin_error, bin_mean, 'mean')

    # variance
    var_a, var_b, var_c = get_regression(bin_error, bin_variance)
    plot_function(var_a, var_b, var_c, bin_error, bin_variance, 'variance')


def get_regression(x_cords: np.array, y_cords: np.array):

    X, Y = [], []
    for i in range(len(x_cords)):
        X.append([1, x_cords[i], x_cords[i]**2])
        Y.append(y_cords[i])

        #X = np.array(((1, x_cords[0], x_cords[0]**2), (1, x_cords[1], x_cords[1]**2), (1, x_cords[2], x_cords[2]**2)))
        #Y = np.array((y_cords[0], y_cords[1], y_cords[2]))

    print(X, Y)
    X_T = np.transpose(X)
    inverse_factor = np.linalg.inv(np.matmul(X_T, X))

    Beta = np.matmul(inverse_factor, X_T).dot(Y)

    return Beta[0], Beta[1], Beta[2]    # c, b, a


def plot_function(a: float, b: float, c: float, bin_error: list, bin_mean: list, title: str):     # y = a + bx + cx^2
    points = 101
    min, max = np.min(bin_error), np.max(bin_error)
    start = min - 0.5*(max-min)
    end = max + 0.5*(max-min)
    step = (end - start)/(points-1)

    x_list, y_list = [], []
    for x in np.arange(start, end, step):
        y = a + b*x + c*(x**2)

        x_list.append(x)
        y_list.append(y)

    plt.plot(x_list, y_list)
    plt.scatter(bin_error, bin_mean)
    plt.title(title)
    # plt.ylim((min(y_list), max(y_list)))
    plt.show()





def test():
    bin_error = np.array([-2.2, -0.9, 0, 1, 2.1])
    bin_mean = np.array([-1, -0.5, 0, 0.7, 1.1])
    bin_variance = np.array([5, 1.2, 0, 2, 3.8])

    fit(bin_error, bin_mean, bin_variance)

x = test()
