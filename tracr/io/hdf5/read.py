#!/usr/bin/env python
"""
Converts HDF5 format data to a Feature object.

INPUT
=====
    Single multilayer hdf5 file of raw intensity data

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
        Assume single file hdf5 file,
    """
    with h5py.File(ifile, 'r') as hdf:
        dset = hdf['tomograph']
        arr = np.transpose(dset[:], axes=(1,2,0))
        if 'pixel size' in dset.attrs.keys():
            return Feature(arr, pixelsize=dset.attrs['pixel size'])
        else:
            return Feature(arr)
