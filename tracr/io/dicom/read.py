#!/usr/bin/env python
"""
A script that converts dicom files to an intensity voxel array
The resulting array is 1000 x 1024 in cross section direction and 1014 "tall"
"""

import sys, os
import numpy as np
import dicom

def read(dcm_files):
	# Import image and details. Input is a list of filename strings
	layer = dicom.read_file(dcm_files[0])
	dicom_array = np.zeros((int(layer.Rows), int(layer.Columns), len(dcm_files)))
	pixel_size = float(layer.PixelSpacing[0])*1000
	for filename in dcm_files:
		layer = dicom.read_file(filename)
		dicom_array[:, :, int(layer.InstanceNumber)-1] = layer.pixel_array
	return dicom_array, pixel_size

if __name__ == '__main__':
	try:
		# generate array
		dicom_array = read(ifile)
		# read filename
		try:
			ofile = sys.argv[2]
		except IndexError:
			path, base = os.path.split(ifile)
			ofile, ext = os.path.splitext(base)
		# save the output
		np.save(path+ofile, dicom_array)
	except:
		sys.stderr.write('Usage: {} INPUT.tif [OUTPUT.npy]'.format(sys.argv[0]))
		sys.exit(1)
