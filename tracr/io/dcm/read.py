#!/usr/bin/env python
"""
Converts .dcm format data to a Feature object.

INPUT:
	- ifile: List of single dcm frame, or list of multiple frames
	- **pixelsize (um/pixel)

OUTPUT:
	- Feature object (array (either 2D or 3D) of .dcm intensity data) and pixel
		size in um/pixel

USAGE:
	e.g. intensity_array = read('path/to/frame.dcm')
	e.g. intensity_array = read('path/to/DCM_folder/')
"""

import sys, os, glob
from warnings import warn
import dicom
import numpy as np
from ...base import Feature

def read_single(ifile):
    return dicom.read_file(ifile).pixel_array

def read(ifile, **kwds):
	# ifile is a list, generate Feature object by iterating through list
	# Pixelsize must be function input (not kwd) by the time we call 'Feature'.
	arr = np.array([dicom.read_file(frame).pixel_array for frame in ifile])
	arr = np.transpose(arr, axes=(1,2,0))

	if 'pixelsize' in kwds:
		px_size = float(kwds['pixelsize'])
	else:
		# Ensure that all frames share similar pixel sizes
		sizes = np.array([dicom.read_file(f).PixelSpacing for f in ifile],
							dtype=float)
		sizes = np.ravel(sizes)
		if not np.allclose(sizes, sizes[0]):
			msg = 'Voxel dimensions are not the same.'
			raise NotImplementedError(msg)
		px_size = 1000*sizes[0]
	warn('Pixelsize for sample {} has been set to: {}'.format(ifile[0], px_size))
	return Feature(arr, pixelsize=px_size)
