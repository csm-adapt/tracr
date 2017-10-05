from __future__ import division
import sys, os
import numpy


"""
INPUT
=====
    larr (ndarray): A labeled array with 'num' clusters of integer values and '0'
                    cluster for passed material (background).

OUTPUT
======
    sigmas (ndarray): An mxn array of sigma values describing scaling in each
                        feature's principal direction.


"""

def svd(coords):
    # center the coordinates at the origin — required for SVD
    center = np.mean(coords, axis=0)
    new_coords = coords - center
    # for nx2 coord array, below returns: (nx2), (2,), (2x2)
    u,s,v = np.linalg.svd(new_coords, full_matrices=False)
    return u, np.diag(s), np.transpose(v)

def eccentricity(larr)
    num = np.max(larr)
    dims = len(larr.shape)
    sigmas = np.zeros((num-1, dims))

    for f in range(1,num):
        coords = np.argwhere(lbl==f).astype(float)
        if len(coords) > 1:
            u,s,v = svd(coords)
            for sig in range(dims):
                sigmas[f,sig] = np.sqrt(s[sig,sig])
    return sigmas
