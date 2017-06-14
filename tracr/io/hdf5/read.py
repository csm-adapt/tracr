#!/usr/bin/env python
"""
Converts HDF5 format data to a Feature object.

INPUT
=====
    Single multilayer hdf5 file of raw intensity data

    The assumed structure of the HDF5 file is:
    GROUP "/" {
        DATASET "tomograph" {
            DATATYPE numeric
            ATTRIBUTE "pixel size" {
                DATATYPE float
            }
            ATTRIBUTE "pixel units" {
                DATATYPE string
            }
        }
    }

By default, the "tomograph" dataset is tranposed from
`[layer, width, height]` order to `[x, y, z]`, where
`x <- width`, `y <- height` and `z <- layer`.


OUTPUT
======
    Feature object

USAGE
=====
    e.g. feat = read('path/to/hdf5_file', pixelsize=px_size)
    * pixelsize has been set in general reading function.
"""

import sys, os, glob
import h5py
from warnings import warn
import logging
import numpy as np
from ...base import Feature


def read(ifile, **kwds):
    """
    Root reading function:
        Assume single file hdf5 file, iterate through list.
    """
    for sample in ifile:
        with h5py.File(sample, 'r') as hdf:
            dset = hdf['tomograph']
            arr = np.transpose(dset[:], axes=(1,2,0))
            if 'pixel size' in dset.attrs.keys():
                return Feature(arr, pixelsize=dset.attrs['pixel size'])
            else:
                return Feature(arr)
