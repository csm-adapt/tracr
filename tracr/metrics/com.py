#!/usr/bin/env python
## A script that calculates the COM of each void detected using scipy.label
## Format oversimplified, will be updated to reflect usage
## Input - intensity_array: the 3D array of intensity data (np.array)
## Output - centers of mass (list of tuples)

import os, sys
import numpy as np
from scipy.ndimage.measurements import label, center_of_mass

"""
Author: Henry Geerlings
Date Created: June 15, 2016
Colorado School of Mines
"""

# Assumes this module will be imported and array is input
def centers_of_mass(intensity_array):
    lbl, num_lbl = label(intensity_array, np.ones((3,3,3)))
    return center_of_mass(intensity_array, lbl, np.arange(2,num_lbl))
