import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from constants import tow_width_specified

# --- importing necessary functions from other files, hopefully names are self-explanatory ---
from Model_ALL_ConsecutiveModeler import run_model as get_sensor_data
from Model_ALL_GapStatistics import generate_multitow_layout as get_overlap_data
from Model_ALL_GapStatistics import get_traverse_data as get_traverse_data


# How I would do this, feel free to do whatever you want though
def get_sensor_distribution():
    '''get the distributions of data for each of the sensors.
        Manuel should already have done this in some other file,
        but we need it in a form we can use for a model'''

def generate_sensor_data():
    '''generate a bunch of random data, not taking into account neighbourhood.
        Probably just some random sampling from the distributions'''

def generate_gaps():
    '''use data to also generate gap_data.
     Might be able to re-se parts of generate_multitow_layout from Model_ALL_GapStatistics.'''


def plot_shit_or_something():
    '''plot it all.
        Might be able to repurpose some stuff from Model_ALL_ConsecutiveModeler and Model_ALL_GapStatistics'''


