#!/usr/bin/env python

"""
DESCRIPTION

    Script for scraping process parameters and defect parameters for PCA
    Outfitted for use with 'process_parameters.csv'
"""

from __future__ import division
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys, os, glob
import numpy as np
import json

def scrape_data(plate_num=['2'], feat_list=None):

    # Retrieve process parameters
    build_data = np.genfromtxt('process_parameters.csv', delimiter=',',
                                    dtype=None)
    # Obtain build features of interest
    if feat_list==None:
        print build_data[0,:]
        feats = raw_input('Please enter build features as a list of strings: ')
    else:
        pass



    for f in glob.glob('*.json'):
        data = json.loads(open(f, 'rb').read())
        ifile = os.path.basename(f)
        processed_parts.append(os.path.splitext(ifile)[0][:3])
