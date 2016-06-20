#!/usr/bin/env python
# The volume swept out by a 3D spherical annulus in a sheet of finite
# thickness is:
#
#     R 2pi pi
#    /` /` /`        /     /          x_min < r sin f cos q < x_max
#   |  |  |         |     \ r sin f   y_min < r sin f sin q < y_max
#   |  |  |          \ r  <
#   |  |  | dr dq df <    / 0         else
#   |  |  |          /    \
#   |  |  |         |
#  ./ ./ ./          \ 0        r cos f < z_min, r cos f > z_max
#  0  0  0

import os
import numpy as np
import ctypes
from scipy import integrate
from skmonaco import mcmiser
from itertools import product, combinations


class TruncatedSphere(object):
    def __init__(self, *args, **kwds):
        """
        Generates a sphere bounded by LOWER from below and
        UPPER from above.

        Parameters (0 or 2)
        ----------
        :lower, DIM-length tuple: Defines the most negative corner.
        :upper, DIM-length tuple: Defines the most positive corner.
        """
        if len(args) == 2:
            lower, upper = args
            assert(len(lower) == 3)
            assert(len(upper) == 3)
            self._lower = np.asarray(lower, dtype=float)
            self._upper = np.asarray(upper, dtype=float)
        else:
            self._lower = -np.ones(3)
            self._upper = np.ones(3)
        parent, filename = os.path.split(os.path.realpath(__file__))
        lib = ctypes.CDLL(parent + '/cintegrands.so')
        self.vintegrand = lib.truncated_volume
        self.vintegrand.restype = ctypes.c_double
        self.vintegrand.argtypes = (ctypes.c_int, ctypes.c_double)

    @property
    def lower(self):
        return self._lower

    def set_lower(self, val, axis=None):
        if axis is None:
            assert len(self.lower) == len(val)
            self._lower = np.asarray(val)
        self._lower[axis] = val

    @property
    def upper(self):
        return self._upper

    def set_upper(self, val, axis=None):
        if axis is None:
            assert len(self.upper) == len(val)
            self._upper = np.asarray(val)
        self._upper[axis] = val

    def shell(self, Rin, Rout, center=np.zeros(3), **kwds):
        """See docstring for volume."""
        Vout = self.volume(Rout, center=center, **kwds)
        Vin = self.volume(Rin, center=center, **kwds)
        return Vout - Vin

    def volume(self, R, center=np.zeros(3), **kwds):
        """
        Returns the volume of the sphere truncated by a fixed bounding box.
        This is originally intended for calculating the actual volume of
        an annulus in the radial distribution function.

        Parameters
        ----------
        :R, float: Spherical radius.

        Keywords
        --------
        :center, array-like: Center of the sphere.
        :kwds, dict: Keywords passed to mcmiser, e.g.

            nprocs, number of processors to use.
            npoints, number of points for the MC integration.
        """
        if np.isclose(R, 0):
            return 0
        def f_mcmiser(phi, theta, r):
            """Integrand for calculating the volume of a bounded sphere."""
            rcf, rsf = r*np.cos(phi), r*np.sin(phi)
            cq, sq = np.cos(theta), np.sin(theta)
            if rcf < zmin: return 0
            if rcf > zmax: return 0
            if (xmin < rsf*cq < xmax) and (ymin < rsf*sq < ymax):
                return r*rsf
            else:
                return 0
        def f_tanh(phi, theta, r):
            """Integrand for calculating the volume of a bounded sphere."""
            rcf, rsf = r*np.cos(phi), r*np.sin(phi)
            cq, sq = np.cos(theta), np.sin(theta)
            alpha = 8
            xfactor = (1 + np.tanh(alpha*(rsf*cq-xmin)))/2 * \
                      (1 - (1 + np.tanh(alpha*(rsf*cq-xmax)))/2)
            yfactor = (1 + np.tanh(alpha*(rsf*sq-ymin)))/2 * \
                      (1 - (1 + np.tanh(alpha*(rsf*sq-ymax)))/2)
            zfactor = (1 + np.tanh(alpha*(rcf-zmin)))/2 * \
                      (1 - (1 + np.tanh(alpha*(rcf-zmax)))/2)
            return xfactor*yfactor*zfactor*r*rsf
        assert len(center) == 3
        center = np.asarray(center)
        xmin, ymin, zmin = self.lower - center
        xmax, ymax, zmax = self.upper - center
        # Optimize
        def polar(adj):
            """
            Returns the polar angle formed at the base of the spherical cap
            at a distance ADJ from the center, or 0 if ADJ > R.
            """
            ratio = np.abs(adj)/R
            ratio[ratio > 1] = 1.0
            return np.arccos(ratio)
        def height(adj):
            """Height of the spherical cap."""
            val = R - np.abs(adj)
            val[val < 0] = 0
            return val
        fmin = polar((xmin, ymin, zmin))
        fmax = polar((xmax, ymax, zmax))
        heights = height((xmin, ymin, zmin, xmax, ymax, zmax))
        if np.all(np.isclose(fmin, 0.0)) and np.all(np.isclose(fmax, 0.0)):
            # all polar angles are zero --> sphere
            print '<sphere>'
            return 4./3.*np.pi*R**3
        elif np.all([(a + b <= np.pi/2) for a,b in combinations(fmin, 2)]) and \
             np.all([(a + b <= np.pi/2) for a,b in combinations(fmax, 2)]):
            # non-zero polar angles, but no overlapping caps
            print '<non-overlapping caps>'
            vol = 4./3.*np.pi*R**3
            for h in heights:
                vol -= np.pi/3 * h**2 * (3*R - h)
            return vol
        # general -- and generally expensive -- method
        # # monte carlo approach for calculating the volume
        # kwds['npoints'] = kwds.get('npoints', 5e5)
        # kwds['nprocs'] = kwds.get('nprocs', 1)
        # vol, err = mcmiser(lambda fqr: f(*fqr),
        #     xl=(0., 0., 0.),
        #     xu=(np.pi, 2*np.pi, R),
        #     **kwds)
        # return vol
        print '<general>'
        vol, err = integrate.nquad(self.vintegrand,
            [[0, np.pi], [0, 2*np.pi], [0, R]],
            args=(8., xmin, ymin, zmin, xmax, ymax, zmax))
        return vol
#end 'class TruncatedSphere(object):'


if __name__ == '__main__':
    from itertools import product
    from time import time

    box = lambda : np.zeros((128, 64, 32))
    bsphere = TruncatedSphere((-1, -0.5, -0.25), (1, 0.5, 0.25))
    lower = bsphere.lower
    width = bsphere.upper - bsphere.lower
    step = width/box().shape
    voxvol = np.prod(step)
    for r in np.linspace(0.2, 2.0, num=7):
        start = time()
        b = box()
        rsq = r*r
        for ijk in product(*map(xrange, b.shape)):
            xyz = lower + step*ijk
            if np.sum(xyz*xyz) < rsq:
                b[tuple(ijk)] = 1
        discreteVolume = np.sum(b)*voxvol
        bsphstart = time()
        integratedVolume = bsphere.volume(r, nprocs=8)
        bsphdelta = time() - bsphstart
        # assert np.isclose(discreteVolume, integratedVolume, rtol=1e-2), \
        #     'Discrete ({}) and integrated ({}) volumes do not match ' \
        #     'for r = {}'.format(discreteVolume, integratedVolume, r)
        if not np.isclose(discreteVolume, integratedVolume, rtol=1e-2):
            print 'FAILED',
        delta = time() - start
        print 'R = {}: {:.3g} ({:.3g}) s, err = {:.3g}'.format(
            r, delta, bsphdelta, np.abs(1 - integratedVolume/discreteVolume))
