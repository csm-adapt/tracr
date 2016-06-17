#
# Returns the eigenvectors of a masked object.
#

from __future__ import division

import numpy as np


def principal(mask, **kwds):
    """
    Returns the principle axes of the object defined by MASK. These are
    the eigenvectors of an SVD of the object, in row-major order.

    Parameters
    ----------
    :mask, boolean array-like: Mask of the object whose principle axes are
         to be found.

    Keywords
    --------
    :svd, bool: Outputs the U, S, and V matrices from the SVD, in
        their natural order, i.e. V is not transposed to be row-major.
    """
    positions = np.transpose(np.where(mask))
    positions = positions - np.mean(positions, axis=0)
    U,S,V = np.linalg.svd(positions)
    if kwds.get('svd', False):
        return U,S,V
    else:
        return np.transpose(V)
