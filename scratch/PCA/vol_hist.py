#!/usr/binenv python
## Script for plotting the histograms of nn, volumes for user specified parts

import sys, os, glob
import numpy as np
from matplotlib import pyplot as plt

def vol_hist(part_list):

    if part_list == "all":
        for f in glob.glob("*.csv"):
            data = np.loadtxt(f, delimiter=',')
            volume = data[:,4]
            volume = np.delete(volume, np.argmax(volume))
            plt.figure()
            plt.hist(volume, bins=500, log=True)
            plt.title(f)
            plt.xlabel('Volume size (um)^3')
            plt.ylabel('Frequency')
        plt.show()
    else:
        for f in part_list:
            data = np.loadtxt(f, delimiter=',')
            volume = data[:,4]
            volume = np.delete(volume, np.argmax(volume))
            plt.figure()
            plt.hist(volume, bins=500, log=True)
            plt.title(f)
            plt.xlabel('Volume size (um)^3')
            plt.ylabel('Frequency')
        plt.show()


# if __name__ == '__main__':
#     print sys.argv[1]
#     vol_hist(sys.argv[1])
