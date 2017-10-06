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
        larr (ndarray): A labeled array with 'num' clusters of integer values and '0'
                        cluster for passed material (background).

    OUTPUT
    ======
        ecc (ndarray): An num x 1 array of ratios of the lowest/highest sigmas
                        for each feature in labeled array.
    """

    num = np.max(larr)
    dims = len(larr.shape)
    ecc = np.zeros((num-1, 1))

    for f in range(1,num+1):
        coords = np.argwhere(lbl==f).astype(float)
        if len(coords) >= dims:
            u,s,v = svd(coords)
            ecc[f] = np.sqrt(s[-1,-1]/s[0,0])
    return ecc
