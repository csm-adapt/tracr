# Author: Andrew Petersen
# Copyright 2016, ADAPT @ Colorado School of Mines

import numpy as np
import scipy as sp
from scipy import spatial


def surface(pores, surface):
	# INPUTS
	# pores = Nx3 numpy array of pore locations
	# surface = Mx3 numpy array of surface points
	#	
	# OUTPUTS
	# dCalcs = Nx2 matrix containing in 1st column, the shortest distance from the pore to
	#	the surface, and in the 2nc column, the index of the corresponding surface point that
	#	gives the shortest distance

	# creates kd tree of surface point cloud
	tree_surface = sp.spatial.KDTree(surface)

	# preallocates memory for the distance calculations for each pore
	dCalcs = np.zeros([pores.shape[0],2],dtype='float64')

	# for every pore, performs a query within the surface kd tree to see
	# which point in the surface is closest to the pore location
	for ir in range(0,pores.shape[0]):
		dCalcs[ir][:] = tree_surface.query(pores[ir][:]);

	return dCalcs;
