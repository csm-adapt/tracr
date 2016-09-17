import sys
sys.path.append('..')
#from tracr import tracr
from tracr.metrics.distance import surface as surface_distance
import numpy as np

# To test, simply run
# [...]$ nosetests (optionally with -v)
# and a report a summary of the results


def mesh_sphere(radius, npts=50):
    """Creates a spherical mesh with NPTS points at the equator."""
    def azimuth_linspace(phi):
        return np.linspace(0, 2*np.pi, np.round(npts*np.cos(phi)))
    pts = [(0, 0, -1)]
    for phi in np.linspace(-np.pi/2, np.pi/2, npts/2):
        z = np.sin(phi)
        r = np.cos(phi)
        pts.extend([(r*np.cos(az), r*np.sin(az), z)
                    for az in azimuth_linspace(phi)])
    pts.append((0, 0, 1))
    pts = radius*np.array(pts)
    return pts


class TestClass: # keep this the same
    def setUp(self):
        # construct objects and perform any necessary setup
        pass

    def test_surface(self):
        # run test one
        radius = float(20)
        # create a sphere of surface points
        sphere = mesh_sphere(radius, npts=100)
        # create a random array of points within the surface
        R, theta, phi = np.random.random((3, 20))
        R = radius*R
        z = np.sin(np.pi/2 * (2*phi - 1))
        x = np.cos(2*np.pi * theta)*z
        y = np.sin(2*np.pi * theta)*z
        cloud = np.dot(np.diag(R), np.transpose((x, y, z)))
        # actual distances
        actualDist = np.linalg.norm(cloud, axis=1)
        # calculated distances
        distances, indices = surface_distance(cloud, sphere)
        assert not np.all(np.isclose(actualDist, distances, rtol=0.01)), \
            '{}'.format(np.array([actualDist,
                                  distances,
                                  actualDist/distances]).T)

    def tearDown(self):
        # clean up
        pass
