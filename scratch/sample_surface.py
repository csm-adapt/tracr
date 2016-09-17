# Script for identifying the sample surface

from __future__ import division
import numpy as np

def sample_surface(intensity_array):
    # INPUT: X x Y x Z sized 3-D array of xct data
    # OUTPUT: list of unique sample surface coordinates

    surface = []

    # iterate through each vertical layer of the image
    for z in range(intensity_array.shape[2]):
        # iterate through the pixels in each layer, detecting surface
        for y in range(intensity_array.shape[1]):
            for x in range(intensity_array.shape[0]):
                if intensity_array[x,y,z] != 0:
                    surface.append([x,y,z])
                    break
        for x in range(intensity_array.shape[0]):
            for y in range(intensity_array.shape[1]-1,-1,-1):
                if intensity_array[x,y,z] != 0:
                    surface.append([x,y,z])
                    break
        for y in range(intensity_array.shape[1]-1,-1,-1):
            for x in range(intensity_array.shape[0]-1,-1,-1):
                if intensity_array[x,y,z] != 0:
                    surface.append([x,y,z])
                    break
        for x in range(intensity_array.shape[0]-1,-1,-1):
            for y in range(intensity_array.shape[1]):
                if intensity_array[x,y,z] != 0:
                    surface.append([x,y,z])
                    break

    # Remove duplicates
    surface = [tuple(coord) for coord in surface]
    return list(set(surface))
