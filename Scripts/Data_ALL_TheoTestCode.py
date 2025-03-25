" Nothing here yet but bro is cooking "

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from Data_CAM_importer import CAM_exceltolist
from Handling_ALL_Functions import get_processed_data

print(get_processed_data(5, "LT"))