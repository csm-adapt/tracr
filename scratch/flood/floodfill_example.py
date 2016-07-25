#!/usr/bin/env python

## Perform a floodfill on a 2D set of data

"""
Author: Henry Geerlings
Date Created: July 17, 2016
Colorado School of Mines
"""

import numpy as np
import sys, os
from matplotlib import pyplot as plt

def makeshape():
    # Generate circular data
    data = np.ones((256,256), dtype=bool)
    clone = np.zeros_like(data)
    center = data.shape[0]/2
    radius = data.shape[0]/3
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            if np.sqrt((x-center)**2 + (y-center)**2) < radius:
            	data[x,y] = False
    return data

def floodfill(data, i,j=[0,0], result=None):

    def fillQ(i,j):
        # Run tests for current coordinate
        rval == np.isclose(data[i,j],0)
        if i >= data.shape[0] or j >= data.shape[1]:
            rval = False
        if rval:
            rval = (result[i,j] != 1)
        return rval

    # Image origin is at top-left
    if i,j == [0,0]:
        result = fillQ(i,j)
    if fillQ(i+1,j):    # Check right
        result = floodfill(data, (i+1,j), result)
    if fillQ(i,j+1):    # Check down
        result = floodfill(data, (i,j+1), result)
    if fillQ(i-1,j):    # Check left
        result = floodfill(data, (i-1,j), result)
    if fillQ(i,j-1):    # Check up
        result = floodfill(data, (i,j-1), result)

    return result
