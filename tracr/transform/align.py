#
# Transforms the numpy array to change alignment, e.g.
# to align the axis of some feature with the z-axis.


from ..distribution.orientation import principal
from itertools import combinations


def image(image, xi, **kwds):
    """
    Rotates image so the axes XI align to XF after rotation. The rotation
    is performed with CENTER as the invariant point.

    In the rotate image, XI will be aligned so that the first axis is
    guaranteed to align along the first axis of XF (default: [0, 0, ..., 1]).
    The other axes may be interchanged to ensure compatible handedness
    between XI and XF.

    Parameters
    ----------
    :image, multidimensional array-like: Image to rotated.
    :xi, orthonormal multidimensional array-like: Axes that span an N-D
        space.

    Keywords
    --------
    :xf, orthonormal multidimensional array-like: Axes to which XI is to be
        aligned after rotation.
        Default: ((0,0,...,1), (1,0,...,0), (0,1,...,0), ..., (0,0...,1,0))
    :center, vector: Invariant center about which the image should be rotated.
    :fill, scalar: value to use to fill the added pixels

    Returns
    -------
    Rotated image
    """
    def handedness(axes):
        """
        Returns the handedness (left/right = -1/1) of the space spanned
        by AXES.
        """
        return np.sign(np.linalg.det(axes))
    def orthonormal(axes):
        """Returns true of the axes are orthonormal. False otherwise."""
        axes = np.asarray(axes)
        dim = axes.shape[0]
        if not np.all(np.equal(axes.shape, dim)):
            msg = "Axes must be a square matrix."
            raise ValueError(msg)
        # check normality
        mag = np.linalg.norm(axes, axis=0)
        # check orthogonality
        proj = [np.dot(axes[i], axes[j]) for i,j in combinations(range(dim), 2)]
        return np.all(np.isclose(mag, 1.0)) and np.all(np.isclose(proj, 0.0))
    # validate the input values
    image = np.asarray(image)
    xi = np.asarray(xi)/np.linalg.norm(xi, axis=0)
    if not orthonormal(xi):
        msg = '{} is not orthonormal.'.format(xi)
        raise ValueError(msg)
    # check that the dimensions match
    dim = len(image.shape)
    if (dim, dim) != xi.shape:
        msg = 'The dimensions of XI, {}, and IMAGE, {}, ' \
              'do not match'.format(xi.shape, dim)
        raise ValueError(msg)
    # process keywords
    if 'xf' not in kwds:
        order = tuple(range(dim))
        order = (order[-1],) + order[:-1] # first rotation
        xf = np.eye(dim)
        xf = np.transpose(xf, axes=order)
    else:
        xf = np.asarray(xf)/np.linalg.norm(xf, axis=0)
        if (dim, dim) != xf.shape:
            msg = 'The dimensions of XF, {}, and IMAGE, {}, ' \
                  'do not match'.format(xi.shape, dim)
            raise ValueError(msg)
    if not orthonormal(xf):
        msg = '{} is not orthonormal.'.format(xf)
        raise ValueError(msg)
    if handedness(xi) != handedness(xf):
        order = tuple(range(dim))
        order = (order[-1],) + order[:-1] # first rotation
        xf = np.transpose(xf, axes=order)
    if 'center' not in kwds:
        center = np.array(image.shape, dtype=float)/2
    else:
        center = np.asarray(center, dtype=float)
    fill = float(kwds.get('fill', 0))
    # from http://math.stackexchange.com/questions/1125203/finding-rotation-axis-and-angle-to-align-two-3d-vector-bases
    # R*a = e; R*b = f ; R*c = g
    # a = longest principle axis
    # b = next longest principle axis
    # c = shortest principle axis
    # e = (0,0,1) (default)
    # f = (0,1,0)
    # g = (1,0,0)
    # R = outer(e,a) + outer(f,b) + outer(g,c)
    # construct the rotation matrix
    R = np.sum([np.outer(a, b) for a,b in zip(xf, xi)])
    # shift to the center (Nxn)
    idx = tuple(xrange(length) for length in mask.shape)
    idx = np.array([ijk for ijk in product(*idx)])
    idx = idx - center
    # perform the rotation
    # (nxn)*(Nxn)^T = (nxN) --> transpose --> (Nxn)
    irot = np.dot(R, idx.T).astype(int).T
    # grow the image
    irot = irot - np.min(irot, axis=0)
    shape = np.max(irot, axis=0)+1
    ijk = tuple(np.transpose(irot))
    rotated = fill*np.ones(shape)
    rotated[ijk] = image
    return rotated
