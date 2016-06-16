#!/usr/bin/env python
## A script that converts ORS saved tif frames to an intensity voxel array
## The resulting array is 1000 x 1024 in cross section direction and 1014 "tall"

import sys, os
import numpy as np
from PIL import Image, ImageSequence
from sklearn.preprocessing import binarize

def read(ifile):
	# Import image and details
    im = Image.open(ifile)
    intensity_array = np.array([np.array(frame) for frame in ImageSequence.Iterator(im)])
    intensity_array = np.transpose(intensity_array, axes=(1,2,0))
	if np.max(intensity_array)>1:
		binarize(intensity_array, threshold=2000, copy=False) # characteristic of air
	intensity_array = (intensity_array==0)
	return intensity_array
#end 'def tif2array(ifile, ofile=None):'

if __name__ == '__main__':
	try:
		# generate array
		intensity_array = read(ifile)
		# read filename
		try:
			ofile = sys.argv[2]
		except IndexError:
			path, base = os.path.split(ifile)
			ofile, ext = os.path.splitext(base)
		# save the output
		np.save(path+ofile, intensity_array)
	except:
		sys.stderr.write('Usage: {} INPUT.tif [OUTPUT.npy]'.format(sys.argv[0]))
		sys.exit(1)
