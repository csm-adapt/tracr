#
# Axes utilities
#

import numpy as np
from itertools import combinations


def dim(axes):
    """Returns the dimensionality of the space spanned by AXES."""
    return len(axes.shape)


def valid_axes(axes):
    """Check that the axes are valid."""
    assert dim(axes) == 2, 'Invalid axes dimensions.'
    assert axes.shape[0] == axes.shape[1], 'Axes vectors do not match.'
    return True


def is_normal(axes):
    """Return True if the axes are normal."""
    valid_axes(axes)
    norms = np.linalg.norm(axes, axes=0)
    return np.all(np.isclose(norms, 1.0))


def is_orthogonal(axes):
    """Returns True if axes are orthogonal."""
    valid_axes(axes)
    d = dim(axes)
    return np.all([np.isclose(np.dot(axes[i], axes[j]), 0.0)
                   for i,j in combinations(range(d), 2)])


def handedness(axes):
    """
    Returns the handedness of the axes. -1 = left handed, +1 right handed,
    or 0 (degenerate).
    """
    valid_axes(axes)
    return np.sign(np.linalg.det(axes))


def normalize(axes, copy=False):
    """
    Normalizes the axes.
    """
    valid_axes(axes)
    if copy:
        axes = np.copy(axes)
    axes[:] /= axes/np.linalg.norm(axes)
    if copy:
        return axes
