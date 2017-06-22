"""
Test script for TRACR Otsu multilevel thresholding algorithm.
"""

import os, sys, glob
import numpy as np
sys.path.append('..')
from tracr.segmentation.threshold import otsu
from matplotlib import pyplot as plt

# NOT YET A TEST - JUST SETUP FOR TOY DATASET
def test_bilevel_visual():

    plt.close()
    # Build vector with two Gaussian humps
    a = 50
    b = 500
    n = 300
    mu, sigma = 0, 0.5

    s = (b-a)*np.random.normal(mu, sigma, n)+a
    t = s + 3000
    u = np.concatenate((s, t))

    thresh_val = otsu(u)
    plt.hist(u, bins=128)
    plt.axvline(thresh_val, color='r')
