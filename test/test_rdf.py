import sys
sys.path.append('..')
#from tracr import tracr
from tracr.distribution import rdf
from itertools import product
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# To test, simply run
# [...]$ nosetests (optionally with -v)
# and a report a summary of the results

class TestClass: # keep this the same
    def setUp(self):
        # construct objects and perform any necessary setup
        pass

    def test_rdf(self):
        low = -5*np.ones(3)
        high = 5*np.ones(3)
        #points = 5*(2*np.random.random((40, 3)) - 1)
        points = np.array([
            ijk for ijk in product(range(-5, 6, 2),
                                   range(-5, 6, 2),
                                   range(-5, 6, 2))],
            dtype=float)
        fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        # ax.scatter(points[:,0], points[:,1], points[:,2])
        # plt.show()
        r,g = rdf(50, points, low=low, high=high)
        print "(r,g) = (\n  {},\n  {})".format(r, g)
        width = r[1] - r[0]
        plt.bar(r, g, width, color='r')
        plt.show()
        assert 1 == 1
