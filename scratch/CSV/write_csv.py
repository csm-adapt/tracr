#!/usr/bin/env python
## script for batch processing XCT void data. Returns csv files.

from __future__ import division
import os, sys
import time
import numpy as np
from pixel_sizes import pixel_dict
from scipy.ndimage.measurements import label, center_of_mass
from read import read
from itertools import product

path = '.'
#files = os.listdir(path)
px_dict = pixel_dict()
#np.seterr(divide='ignore', invalid='ignore')

#for ifile in files:
for ifile in sys.argv[1:]:
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

        print("finding part com")
        part_com = np.mean(np.argwhere(lbl==0), axis=0)

        print('find blobs')
        #blobs = [(i, np.argwhere(lbl==i)) for i in range(2,num+1)]
        try:
            start = time.time()
            indices = np.argwhere(lbl > 1)
            blobs = [[] for _ in range(num-1)]
            for i,j,k in indices:
                l = lbl[i,j,k]
                blobs[l-2].append((i,j,k))
            ss = time.time() - start
            mm = ss//60 ; ss -= 60*mm
            print("blob detection: {:.0f}:{}".format(mm, ss))
            #print("voxels per pore: {}".format([len(b) for b in blobs]))
        except Exception:
            ss = time.time() - start
            mm = ss//60 ; ss -= 60*mm
            msg = '\n'.join([
                "<BLOB>"
                "  indices = {}".format(indices),
                "  runtime = {:.0f}:{}".format(mm, ss),
                "  (i,j,k) = ({}, {}, {})".format(i, j, k),
                "</BLOB>\n"])
            sys.stderr.write(msg)
            raise
        # blobs = (num-1)*[[]]
        # shape = intensity_array.shape
        # counter = 0
        # niter = np.product(shape)
        # for ijk in product(range(shape[0]), range(shape[1]), range(shape[2])):
        #     l = lbl[ijk]
        #     if l < 2: continue # skip sample and ambient air
        #     blobs[l-2].append(ijk)
        #     counter += 1
        #     if niter/counter == niter//counter:
        #         if niter//counter % 10 == 0:
        #             print('|{}%|'.format(niter//counter), end='')
        #         elif niter//counter % 2 == 0:
        #             print('-', end='')
        # print('')

        print('getting coms')
        com = np.array([np.mean(b, axis=0) for b in blobs])
        # shift com
        com = com - part_com
        # com = center_of_mass(intensity_array, lbl, np.arange(2,num))
        # com = np.asarray(com)
        com = px*com

        print('getting volumes')
        volume = np.array([len(b) for b in blobs])
        # volume = np.array([
        #     np.sum(lbl == i)
        #     for i in range(2,num)
        # ])
        volume = px*px*px*volume

        print('writing file')
        table = np.concatenate((np.arange(1,num).reshape((num-1,1)),com,volume.reshape((num-1,1))), axis=1)
        np.savetxt(name+'.csv', table, delimiter=',', fmt=['%d', '%g' ,'%g', '%g', '%g'])
