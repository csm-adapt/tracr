# Script for identifying the sample surface

from __future__ import division
import numpy as np

def sample_surface(intensity_array):
    # INPUT: X x Y x Z sized 3-D array of xct data
    # OUTPUT: list of sample surface coordinates

    surface = []

    # iterate through each vertical layer of the image
    for z in range(intensity_array.shape[2]):

        # iterate through the pixels in each layer, detecting surface
        for x in range(intensity_array.shape[0]):
            for y in range(intensity_array.shape[1]):
                if intensity_array[x,y,z] != 0:
                # to be continued...
