# -*- coding: utf-8 -*-
from __future__ import division
import sys, os
import numpy

def svd(coords):
    # center the coordinates at the origin — required for SVD
    center = np.mean(coords, axis=0)
    new_coords = coords - center
    # for nx2 coord array, below returns: (nx2), (2,), (2x2)
    u,s,v = np.linalg.svd(new_coords, full_matrices=False)
    return u, np.diag(s), np.transpose(v)

def eccentricity(larr):

    """
    INPUT
    =====
        - larr (ndarray): A labeled array with 'num' clusters of integer values and '0'
                        cluster for passed material (background).

    OUTPUT
    ======
        - ecc (ndarray): An num x 1 array of ratios of the lowest/highest sigmas
                        for each feature in labeled array.
    """

    num = np.max(larr)
    dims = len(larr.shape)
    ecc = np.zeros((num-1, 1))

    if dims == 2:
        for f in range(1,num+1):
            coords = np.argwhere(lbl==f).astype(float)
            if len(coords) >= dims:
                u,s,v = svd(coords)
                s1 = np.sqrt(s[0,0])
                s2 = np.sqrt(s[1,1])
                ecc[f] = 1 - s2/s1
        return ecc
    elif dims == 3:
        for f in range(1,num+1):
            coords = np.argwhere(lbl==f).astype(float)
            if len(coords) >= dims:
                u,s,v = svd(coords)
                s1 = np.sqrt(s[0,0])
                s2 = np.sqrt(s[1,1])
                s3 = np.sqrt(s[2,2])
                ecc[f] = 0.5*((1-sc2/sc1) + (1-sc3/sc1))
        return ecc
    else:
        raise IndexError('Dimension of dataset is neither 2 or 3.')
