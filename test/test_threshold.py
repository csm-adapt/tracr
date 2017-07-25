"""
Test script for TRACR Otsu multilevel thresholding algorithm.
"""

import os, sys, glob
import numpy as np
sys.path.append('..')
from tracr.segmentation.threshold.multilevel import otsu
from matplotlib import pyplot as plt
from skimage import data

# NOT YET A TEST - JUST SETUP FOR TOY DATASET
def test_bilevel_random():
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
    plt.close()
    plt.hist(u, bins=256)
    plt.axvline(thresh_val, color='r')
    plt.show()

def test_bilevel_camera():
    cam = data.camera()
    thresh_val = otsu(cam.flatten())

    f, axarr = plt.subplots(2,2)
    axarr[0,0].imshow(cam, cmap="gray")
    axarr[1,0].hist(cam.flatten(), bins=256)
    axarr[0,1].imshow(cam > thresh_val, cmap="gray")
    axarr[1,1].hist(cam.flatten(), bins=256)
    axarr[1,1].axvline(thresh_val, color="r")
    plt.show()
