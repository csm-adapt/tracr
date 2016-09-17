# Returns a list of void volumes (pixels) in order determined by labeled array.
import numpy as np

def pore_volume(porosity):
    vols = np.array([
        np.sum(p)
        for p in porosity
    ])
    return vols
