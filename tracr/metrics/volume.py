# Returns a list of void volumes (pixels) in order determined by labeled array.
import numpy as np

def volume(larr):

    """
    INPUT
    =====
        - larr (ndarray): A labeled array with 'num' clusters of integer values and '0'
                        cluster for passed material (background).

    OUTPUT
    ======
        - vols (list): An 'n+1' list of voxel volumes corresponding to labels from 'arr'.

    """
    num = larr.max()
    vols = np.zeros(num+1)
    np.add.at(vols, larr.flat, 1)
    return vols
