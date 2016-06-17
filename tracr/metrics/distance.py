# Author: Andrew Petersen
# Copyright 2016, ADAPT @ Colorado School of Mines

import numpy as np
# import scipy as sp
# from scipy import spatial
from scipy.spatial import cKDTree


def surface(points, surface):
	# INPUTS
	# points = Nx3 numpy array of feature (e.g. pore) locations
	# surface = Mx3 numpy array of surface points
	#
	# OUTPUTS
	# (distance, indices) the shortest distance from the feature to the
	# surface, and in the 2nd item, the indices of the corresponding surface
	# points that gives the shortest distance

	# creates kd tree of surface point cloud
	tree_surface = cKDTree(surface)

	# calculate nearest neighbor distances
	distance, indices = tree_surface.query(points, n_jobs=-1)

	# # preallocates memory for the distance calculations for each pore
	# dCalcs = np.zeros([pores.shape[0], 2], dtype=float)
	#
	# # for every pore, performs a query within the surface kd tree to see
	# # which point in the surface is closest to the pore location
	# for ir in range(0,pores.shape[0]):
	# 	dCalcs[ir][:] = tree_surface.query(pores[ir][:])

	return (distance, indices)
