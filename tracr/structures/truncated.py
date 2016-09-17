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
            assert(len(lower) == 3)
            assert(len(upper) == 3)
            self._lower = np.asarray(lower, dtype=float)
            self._upper = np.asarray(upper, dtype=float)
        else:
            self._lower = np.zeros(3)
            self._upper = np.zeros(3)
        # C integrand function for numerical integration
        # compile in this directory using the (OS specific)
        # compiler command, e.g. for Linux/Mac OS:
        #
        #   gcc -shared -o cintegrands.so -fPIC -lm cintegrands.c
        #
        parent, filename = os.path.split(os.path.realpath(__file__))
        ofile = parent + '/cintegrands.so'
        try:
            open(ofile, 'r').close()
        except IOError:
            import subprocess
            ifile = parent + '/cintegrands.c'
            try:
                open(ifile).close()
            except IOError:
                msg = "Could not compile {}. File not found.".format(ifile)
                raise IOError(msg)
            print '{} was not found. Attempting to ' \
                  'compile {}...'.format(ofile, ifile)
            subprocess.call([
                'gcc',
                '-shared',
                '-o {}'.format(ofile),
                '-fPIC',
                '-lm',
                ifile])
        lib = ctypes.CDLL(parent + '/cintegrands.so')
        self.vintegrand = lib.truncated_volume
        self.vintegrand.restype = ctypes.c_double
        self.vintegrand.argtypes = (ctypes.c_int, ctypes.c_double)

    @property
    def dim(self):
        return 3

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
        if isinstance(Vout, tuple) or isinstance(Vin, tuple):
            msg = '\n'.join([
                "Vout: {}, Rout: {}".format(Vout, Rout),
                "Vin: {}, Rin: {}".format(Vin, Rin)])
            raise ValueError(msg)
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
        """
        R = float(R)
        if np.isclose(R, 0):
            return 0
        assert len(center) == 3
        center = np.asarray(center)
        # distance from center to edge
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
            vol = 4./3.*np.pi*R**3,
        elif np.all([(fmin[i] + fmin[j] <= np.pi/2)
                     for i,j in combinations(range(self.dim), 2)]) and \
             np.all([(fmin[i] + fmax[j] <= np.pi/2)
                     for i,j in combinations(range(self.dim), 2)]) and \
             np.all([(fmax[i] + fmin[j] <= np.pi/2)
                     for i,j in combinations(range(self.dim), 2)]) and \
             np.all([(fmax[i] + fmax[j] <= np.pi/2)
                     for i,j in combinations(range(self.dim), 2)]):
            # non-zero polar angles, but no overlapping caps
            vol = 4./3.*np.pi*R**3
            for h in heights:
                vol -= np.pi/3 * h**2 * (3*R - h)
        else:
            # general -- and generally expensive -- method
            vol, err = integrate.nquad(self.vintegrand,
                [[0, np.pi], [0, 2*np.pi], [0, R]],
                args=(8., xmin, ymin, zmin, xmax, ymax, zmax))
        # return the value. It is showing up as a tuple. I don't know why
        # and need to figure that out, but only after I get this running.
        try:
            return vol[0]
        except TypeError:
            return vol
#end 'class TruncatedSphere(object):'
