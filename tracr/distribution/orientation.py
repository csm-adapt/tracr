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


def test_principal():
    from itertools import product, combinations
    imax, jmax, kmax = 128, 128, 128
    field = np.zeros((imax, jmax, kmax), dtype=bool)
    # create an axis-aligned ellipse
    xaxis = np.sqrt(128)
    yaxis = np.sqrt(112)
    zaxis = np.sqrt(96)
    for i,j,k in product(xrange(imax), xrange(jmax), xrange(kmax)):
        r  = ((float(i)-imax//2)/xaxis)**2
        r += ((float(j)-jmax//2)/yaxis)**2
        r += ((float(k)-kmax//2)/zaxis)**2
        if r < 1:
            field[i,j,k] = True
    # randomly rotate the ellipse
    thetaPhiPsi = np.pi/2. * np.random.random(size=(3,))
    cq, cf, cs = np.cos(thetaPhiPsi)
    sq, sf, ss = np.sin(thetaPhiPsi)
    D = np.array([
        [ cf, sf,  0],
        [-sf, cf,  0],
        [  0,  0,  1]])
    C = np.array([
        [  1,  0,  0],
        [  0, cq, sq],
        [  0,-sq, cq]])
    B = np.array([
        [ cs, ss,  0],
        [-ss, cs,  0],
        [  0,  0,  1]])
    A = np.dot(B, np.dot(C, D))
    if not (np.all(np.isclose(np.linalg.norm(A, axis=0), np.ones(3))) and
            np.all(np.isclose(np.linalg.norm(A, axis=1), np.ones(3)))):
        raise ValueError("Rotation matrix for {} " \
                         "is not normal.".format(thetaPhiPsi))
    if not np.all([np.isclose(np.dot(A[i],A[j]), 0) for i,j in
                   combinations(range(3), 2)]):
        proj = ['{}: {}'.format((i,j), np.dot(A[i], A[j]))
                for i,j in combinations(range(3), 2)]
        raise ValueError("Rotation matrix\n{}\nis " \
                         "not orthogonal.\n{}".format(A, proj))
    ## rotate the ellipse
    ijk = np.transpose(np.where(field))
    offset = np.mean(ijk, axis=0)
    ijk = ijk - offset
    ijk = np.dot(A, ijk.T).T
    ijk = (offset + ijk).astype(int).T
    field[:] = False # reset field to empty
    field[ijk[0], ijk[1], ijk[2]] = True
    ## rotate the coordinate axes
    # check
    trueAxes = np.dot(A, np.eye(3)) # these should be the eigenvectors
    testAxes = principle(field) # these are the calculated eigenvectors
    # check
    check = np.all(np.isclose(np.abs(trueAxes), np.abs(testAxes), rtol=0.075))
    if not check:
        assert False, '\n{} != \n{}'.format(trueAxes, testAxes)
    else:
        return True


if __name__ == '__main__':
    test_principal()
