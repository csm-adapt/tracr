## script for batch processing XCT void data. Returns csv files.

from __future__ import division
import os, sys
import numpy as np
from pixel_sizes import pixel_dict
from scipy.ndimage.measurements import label, center_of_mass
from read import read

path = '.'
files = os.listdir(path)
px_dict = pixel_dict()
#np.seterr(divide='ignore', invalid='ignore')

for ifile in files:
    print('Processing {}...'.format(ifile))
    if ifile.endswith(".tif"):

        print('getting pixel sizes')
        [name, ext] = os.path.splitext(ifile)
        px = px_dict[name]

        print('converting to array')
        intensity_array = read(ifile)

        print('binarizing')
        intensity_array = (intensity_array < 2000)

        print('getting void labels')
        lbl, num = label(intensity_array, np.ones((3,3,3)))

        print('find blobs')
        blobs = [(i, np.argwhere(lbl==i)) for i in range(2,num+1)]


        print('getting coms')
        com = np.array([np.mean(b[1], axis=0) for b in blobs])
        # com = center_of_mass(intensity_array, lbl, np.arange(2,num))
        # com = np.asarray(com)
        com = px*com

        print('getting volumes')
        volume = np.array([b[1].shape[0] for b in blobs])        
        # volume = np.array([
        #     np.sum(lbl == i)
        #     for i in range(2,num)
        # ])
        volume = px*px*px*volume

        print('writing file')
        np.save(name+'com', com)
        np.save(name+'vol', volume)
        table = np.concatenate((np.arange(2,num).reshape((num-2,1)),com,volume.reshape((num-2,1))))
        np.savetxt(name+'.csv', table, delimeter=',')
