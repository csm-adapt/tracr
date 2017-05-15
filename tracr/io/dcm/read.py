#!/usr/bin/env python
"""
A script that converts DCM formatted data into a numpy array of intensity
values. Iteratively processes each .dcm layer at a time (no multilayer).
Output 3D arrays are transposed for z-upward indexing.

INPUT:
	- Either a single .dcm file or folder of .dcm frames

OUTPUT:
	- Feature object (array (either 2D or 3D) of .dcm intensity data).

USAGE:
	e.g. intensity_array = read('path/to/frame.dcm')
	e.g. intensity_array = read('path/to/DCM_folder/')
"""

import sys, os, glob
import dicom
import numpy as np
from ..base import Feature

def read_single(ifile):
    return dicom.read_file(ifile).pixel_array

def read(ifile, **kwds):
	# Get pixelsize passed from general reading function
	px_size = kwds.get('pixelsize', 1)

	# If input is folder, iterate through each frame and then transpose 3D array
    if os.path.isdir(ifile):
        all_frames = glob.glob(os.path.join(ifile, '*dcm'))
        return Feature(np.transpose(np.array([read_single(frame) for frame in all_frames]),
                                        axes=(1,2,0)), pixelsize=px_size)
    else:
        return Feature(read_single(ifile), pixelsize=px_size)

if __name__ == '__main__':
    try:
        # Load inputs and read ifile normally
        ifile = sys.argv[1]
        path, base = os.path.split(ifile)
        intensity_array = read(ifile)
        try:
            ofile = sys.argv[2]
        except IndexError:
            # Extract path for saving array
            ofile, ext = os.path.splitext(base)
        np.save(path+'_'+ofile, intensity_array)
    except IndexError:
		sys.stderr.write('CL Usage: python {} [path/to/ifile] [ofile_name]'.format(sys.argv[0]))
		sys.exit(1)
