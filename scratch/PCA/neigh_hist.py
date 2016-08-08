#!/usr/binenv python
## Script for plotting the histograms of nn, volumes for user specified parts

import json
import sys, os, glob
import numpy as np
from matplotlib import pyplot as plt

def neigh_hist(part_list):

    if part_list == "all":
        for f in glob.glob("*.json"):
            data = json.loads(open(f, 'rb').read())
            neigh_list = data['nearest neighbor distance'].values()[1]
            plt.figure()
            plt.hist(neigh_list, bins=500, log=True)
            plt.title(f)
            plt.xlabel('Neighbor Distance (um)')
            plt.ylabel('Frequency')
        plt.show()
    else:
        for f in part_list:
            data = json.loads(open(f, 'rb').read())
            neigh_list = data['nearest neighbor distance'].values()[1]
            plt.figure()
            plt.hist(neigh_list, bins=500)
            plt.title(f)
            plt.xlabel('Neighbor Distance (um)')
            plt.ylabel('Frequency')
        plt.show()


if __name__ == '__main__':
    print sys.argv[1]
    neigh_hist(sys.argv[1])
