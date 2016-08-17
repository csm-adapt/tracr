#!/usr/bin/env python
"""
A script that converts dicom files to an intensity voxel array
The resulting array is 1000 x 1024 in cross section direction and 1014 "tall"
"""

import sys, os, re
import numpy as np
import dicom


def _regularize_dcm_files(dcm_files):
	# Are we reading a file, a list of files, or files from a directory?
	# 1. Is dcm_files a string?
	if isinstance(dcm_files, str):
		# yes: either a single file or a directory
		if os.path.isdir(dcm_files):
			# create a list of DICOM files from the contents of the directory
			# dcm_files = dcm_files.rstrip('/')
			rval = ['{}/{}'.format(dcm_files, fname)
					for fname in os.listdir(dcm_files)
					if re.match(r'.*\.dcm', fname)]
		else:
			# it is it's own file
			rval = [dcm_files]
	else:
		# We receive a list of string filenames, what `read` expects
		rval = dcm_files
	# IOError : ----- WORK IN PROGRESS -----
	# 1) Actual IOError message throws a separate error
	# 2) Depending on rval, this usually always throws errors since `rval` ...
		   # ... is no better than a list of strings unless we are in the dir
	# for fname in rval:
		# if not os.path.isfile(fname):
			# the below IOError threw an error
			# raise IOError('{} is not a file'.format fname)
	return rval


def read(dcm_files):
	"""
	Read DICOM formatted file(s).

	Input
	-----
	:dcm_files, str|iterable: DICOM file(s) to process. This understands
		three use cases:

		1. `dcm_files` is a single DICOM file
		2. `dcm_files` is a list of DICOM files
		3. `dcm_files` is a directory containing DICOM files

	Returns
	-------
	Tuple: (3D numpy array of intensities, pixel size)
	"""
	dcm_files = _regularize_dcm_files(dcm_files)
	dicom_array = None
	for filename in dcm_files:
		layer = dicom.read_file(filename)
		if dicom_array is None:
			nrows, ncols = int(layer.Rows), int(layer.Columns)
			dicom_array = np.zeros((nrows, ncols, len(dcm_files)))
			pixel_size = 1000*np.array(layer.PixelSpacing).astype(float)
		if len(dcm_files)==1:
			dicom_array[:, :, 0] = layer.pixel_array
		else:
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
