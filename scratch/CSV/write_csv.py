## script for batch processing XCT void data. Returns csv files.

from __future__ import division
import os, sys
import numpy as np
from pixel_sizes import pixel_dict
from scipy.ndimage.measurements import label, center_of_mass
from read import read

path = './*.tif'
files = os.listdir(path)
px_dict = pixel_dict()

for file in files:

    #get pixel sizes
    px = px_dict[file]

    # convert to array
    intensity_array = read(file)

    # do final thresholding (1's and 0's)
    intensity_array = (intensity_array < 2000)

    # get void stats
    lbl, num = label(intensity_array, np.ones((3,3,3)))

    com = center_of_mass(intensity_array, lbl, np.arange(num))
    com = np.asarray(com)
    com = px*com

    volume = np.array([
        np.sum(lbl == i)
        for i in xrange(num)
    ])
    volume = px*px*px*volume

    table = np.concatenate((np.arange(num),com,volume))
    np.savetxt(file+'.csv', table, delimeter=',')
