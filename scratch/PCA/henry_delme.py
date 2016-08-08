#!/usr/bin/env python
#
# Returns the median first nearest neighbor pore-pore distance for
# the given CSV file, which is assumed to have columns:
#
#   PoreID, X, Y, Z, volume
#
# where X, Y and Z are the COM positions of the pore with ID PoreID
#

import os, sys
import numpy as np
from scipy.spatial import cKDTree as KDTree
import json


def hist(nndist, **kwds):
    if 'output' in kwds:
        import matplotlib
        matplotlib.use('Agg')
    from matplotlib import pyplot as plt

    # handle formatting keywords
    linewidth = kwds.get('linewidth', 3)
    #plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    n, bins, patches = plt.hist(nndist, normed=True, bins=100)
    width = bins[1] - bins[0]
    ax1 = plt.gca()
    ax2 = plt.twinx()
    ax2.plot(bins[:-1], width*np.cumsum(n), 'r-', linewidth=linewidth)
    ax2.set_ylim(top=1.0)
    tics = ax1.get_yticks(); ax1.set_yticks(tics[1:])
    tics = ax2.get_yticks(); ax2.set_yticks(tics[1:])
    ax1.set_xlabel(r"d ($\mu$m)")
    ax1.set_ylabel(r"PDF")
    ax2.set_ylabel(r"CDF", color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    # check scalar descriptors
    median_dist = np.median(nndist)
    ax1.axvline(median_dist, color='gray', linewidth=linewidth)
    # handle keywords
    if 'title' in kwds:
        plt.title(kwds['title'])
    if 'output' in kwds:
        plt.draw()
        plt.savefig(kwds['output'])
    else:
        plt.show()

def main():
    # read in the file
    try:
        ifs = open(sys.argv[1])
        sample, ext = os.path.splitext(sys.argv[1])
    except IndexError:
        ifs = sys.stdin
        sample = ''
    data = np.loadtxt(ifs, delimiter=',')
    if ifs is not sys.stdin:
        ifs.close()
    # view of the com
    com = data[:,1:4]
    # construct a KD tree
    tree = KDTree(com)
    # query KD tree to find the first nearest neighbor
    dist, idx = tree.query(com, k=2)
    nn = [(i, j, d2) for ((d1, d2), (i, j)) in zip(dist, idx)]
    # histogram of the nearest neighbor distance
    hist(np.array(nn)[:,2])
         #title='{} pore-pore distances'.format(sample),
         #output='{}.pdf'.format(sample))
    # save the nearest neighbor distance to .json files
    ofile = '{}_pore-distribution.json'.format(sample)
    medianDist = np.median(np.array(nn)[:,2])
    cmp0 = lambda lhs, rhs: -1 if lhs[0] < rhs[0] else \
        (1 if lhs[0] > rhs[0] else 0)
   # dist = {
   #     'Pore ID' : list(data[:,0].astype(int)),
   #     'center of mass X' : {
   #         'units' : '$\mu$m',
   #         'values' : list(data[:,1])},
   #     'center of mass Y' : {
   #         'units' : '$\mu$m',
   #         'values' : list(data[:,2])},
   #     'center of mass Z' : {
   #         'units' : '$\mu$m',
   #         'values' : list(data[:,3])},
   #     'volume' : {
   #         'units' : '$\mu$m^3',
   #         'values' : list(data[:,4])},
   #     'nearest neighbor distance' : {
   #         'units' : '$\mu$m',
   #         'values' : [entry[2] for entry in sorted(nn, cmp=cmp0)]},
   #     'median nearest neighbor distance' : {
   #         'units' : '$\mu$m',
   #         'values' : medianDist}
   # }
   # json.dump(dist, open(ofile, 'w'))


if __name__ == '__main__':
    main()

