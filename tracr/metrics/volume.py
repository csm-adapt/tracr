#!/usr/bin/env python
## A script that calculates the volume of each void detected
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
def volumes(intensity_array):
    lbl, num_lbl = label(intensity_array, np.ones((3,3,3)))
    return np.array([
        np.sum(lbl == i)
        for i in xrange(num_lbl)
    ])
