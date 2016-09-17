from ..structures import TruncatedSphere
import numpy as np
from itertools import product
from scipy.spatial import cKDTree as KDTree
import warnings


class RDF(object):
    def __init__(self, nbins, **kwds):
        """
        Create a new RDF object from the point cloud, PTS.

        Parameters
        ----------
        :nbins, int: Number of bins in the RDF.

        Keywords
        --------
        :points, NxDIM array-like: Set the point cloud for the RDF.
        :low, array-like: Set the lower bound along each axis in which PTS
            exists. Default: np.min(pts, axis=0).
        :high, array-like: Set the upper bound along each axis in which PTS
            exists. Default: np.max(pts, axis=0).
        :rmax, float: Maximum R to be considered in the RDF. Default: 'all'
        :fixed, array-like: Axes indices where point-to-point distances
            are calculated as the fixed distance. The special value 'all'
            applies this method to all axes.
        :periodic, array-like: Axes indices where point-to-point distances
            are calculated periodically. The special value 'all' applies
            this method to all axes.
        """
        self._rdf = np.zeros(int(nbins), dtype=float)
        self._periodic = self.dim*[False]
        # volume calculator
        self._truncatedSphere = TruncatedSphere()
        if kwds.has_key('points'):
            self.set_points(kwds['points'])
            self.limits(lower=kwds.get('low', np.min(self.points, axis=0)),
                        upper=kwds.get('high', np.max(self.points, axis=0)))
        else:
            if 'low' in kwds:
                self.limits(lower=kwds['low'])
            if 'high' in kwds:
                self.limits(upper=kwds['high'])
        self._distance = 3*[None]
        for i in range(3):
            self.set_fixed(i)
        if kwds.has_key('rmax'):
            self.set_rmax(kwds['rmax'])
        # set the boundary conditions
        kwds['fixed'] = kwds.get('fixed', 'all')
        if kwds['fixed'] == 'all':
            kwds['fixed'] = range(self.dim)
        for i in kwds['fixed']:
            self.set_fixed(i)
        if kwds.has_key('periodic'):
            if kwds['periodic'] == 'all':
                kwds['periodic'] = range(self.dim)
            for i in kwds['periodic']:
                self.set_periodic(i)

    def __call__(self):
        """Returns the current RDF."""
        r = self.step * np.arange(len(self._rdf)).astype(float)
        return (r, self._rdf)

    def calculate(self, **kwds):
        """
        Calculate the RDF for the current RDF settings.

        Keywords are passed to TruncatedSphere.shell(...)
        """
        rho = float(len(self.points))/np.prod(self.width)
        assert rho > 0, 'Calculated rho ({}) is invalid'.format(rho)
        # reset RDF
        self._rdf[:] = 0
        # create periodic duplicates of the point cloud to facilitate
        # periodic boundary conditions. This can introduce issues for high
        # aspect ratio cells and search space greater than the width of
        # the cell, but for the types of systems we are looking at, this
        # approximation is sufficient.
        points = np.copy(self.points)
        for i in range(len(self.is_periodic())):
            if not self.is_periodic()[i]: continue
            trans = self.upper[i] - self.lower[i]
            points = np.concatenate((points - trans, points, points + trans))
        tree = KDTree(points, leafsize=3)
        # find neighbors
        for i in xrange(self.points.shape[0]):
            pt1 = self.points[i]
            # volume and point count
            vol = self._rdf.shape[0]*[None]
            num = np.zeros_like(self._rdf)
            # for all other points
            # Note: we can't loop over all points greater than... because
            # though the distance is the same, the volume may be different
            # due to boundary conditions.
            indices = tree.query_ball_point(pt1, self.rmax)
            for j in indices:
                pt2 = points[j]
                if np.all(np.isclose(pt1, pt2)):
                    continue
                # distance between the points
                delta = self.distance(pt1, pt2)
                # calculate the radius...
                radius = np.sqrt(np.dot(delta, delta))
                # ... index
                idx = int(radius/self.step)
                # and if no other atom has been found in this volume
                if vol[idx] is None:
                    # calculate the volume of this annulus
                    Rlo, Rhi = self.step*idx, self.step*(idx+1)
                    try:
                        vol[idx] = self._truncatedSphere.shell(Rlo, Rhi, pt1, **kwds)
                    except Exception, e:
                        msg = 'Volume calculation failed at annulus ' \
                              '[{}, {}] around point {}.'.format(Rlo, Rhi, pt1)
                        raise type(e)(msg)
                    if np.isclose(vol[idx], 0):
                        msg = 'Volume is too close to zero ({}) at ' \
                              'annulus [{}, {}] around point {}.'.format(
                                vol[idx], Rlo, Rhi, pt1)
                        raise RuntimeError(msg)
                # increment the number of atoms in this annulus
                num[idx] += 1
            vol = np.array([(1. if (v is None) else v) for v in vol])
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('error')
                    self._rdf += num/vol
            except Exception, e:
                msg = '\n'.join([
                    "({}, {})[{}, {}]:".format(i, j, pt1, pt2),
                    "  num = {}".format(num),
                    "  vol = {}".format(vol)])
                raise type(e)(msg)
        self._rdf /= len(self.points) # average density
        self._rdf /= rho # normalized by the global density
        return self._rdf

    def distance(self, pt1, pt2):
        # to scaled
        dx = (pt2 - pt1)/self.width
        # this applies periodic boundary conditions
        dx = dx - 0.5
        dx = dx - np.ceil(dx)*self.is_periodic()
        dx = dx + 0.5
        # back to real
        return (dx * self.width)
        # return np.array([self._distance[i](pt1, pt2) for i in range(self.dim)])

    def is_fixed(self):
        return ~self._periodic

    def set_fixed(self, axis):
        lower, upper = self.limits()
        self._truncatedSphere.set_lower(lower[axis], axis)
        self._truncatedSphere.set_upper(upper[axis], axis)
        self._periodic[axis] = False
        # self._distance[axis] = dist
        self._rdf[:] = 0

    def is_periodic(self):
        return self._periodic

    def set_periodic(self, axis):
        self._truncatedSphere.set_lower(-np.inf, axis)
        self._truncatedSphere.set_upper(np.inf, axis)
        self._periodic[axis] = True
        # self._distance[axis] = dist
        self._rdf[:] = 0

    def set_points(self, pts):
        self.points = np.asarray(pts)
        self._dim = self.points.shape[-1]
        self._rdf[:] = 0

    def set_rmax(self, val):
        if val == 'all':
            bw = self.width
            self._rmax = lambda : np.sqrt(np.sum(bw*bw))
        else:
            self._rmax = lambda : float(val)
        self._rdf[:] = 0
        self._step = self.rmax/(self._rdf.size + 1)

    def limits(self, lower=None, upper=None):
        # lower
        if lower is not None:
            assert len(lower) == self.dim, \
                'RDF lower bounds must match the RDF dimension'
            self._lower_bound = np.asarray(lower)
            self._truncatedSphere.set_lower(lower)
            self._rdf[:] = 0
            if hasattr(self, '_upper_bound'):
                self._bound_width = self._upper_bound - self._lower_bound
        # upper
        if upper is not None:
            assert len(upper) == self.dim, \
                'RDF upper bounds must match the RDF dimension'
            self._upper_bound = np.asarray(upper)
            self._truncatedSphere.set_upper(upper)
            self._rdf[:] = 0
            if hasattr(self, '_lower_bound'):
                self._bound_width = self._upper_bound - self._lower_bound
        # neither lower or upper are specified
        if lower is None and upper is None:
            return (getattr(self, '_lower_bound', None),
                    getattr(self, '_upper_bound', None))

    @property
    def width(self):
        return getattr(self, '_bound_width', None)

    @property
    def dim(self):
        return getattr(self, '_dim', 3)

    @property
    def rmax(self):
        return self._rmax()

    @property
    def step(self):
        return self._step
#end 'class RDF(object):'


def rdf(nbins, points, **kwds):
    """
    Calculates the pair correlation function of a point cloud.

    Parameters
    ----------
    :nbins, int: Number of bins in the RDF.
    :points, Nx3 array-like: Points that should be used to calculate the RDF.

    Keywords
    --------
    :low, array-like: Bottom left corner of the domain.
    :high, array-like: Top right corner of the domain.
    """
    kwds['points'] = points
    pcf = RDF(nbins, **kwds)
    pcf.set_fixed(0)
    pcf.set_fixed(1)
    pcf.set_fixed(2)
    pcf.set_rmax(5)
    pcf.calculate(nprocs=8)
    return pcf()
