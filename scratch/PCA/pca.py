#!/usr/bin/env python

"""
DESCRIPTION

    Script for scraping process parameters and defect parameters for PCA
    Outfitted for use with 'process_parameters.csv'
"""

from __future__ import division
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import sys, os, glob
import numpy as np
import json


def scrape_data(plate_list=['1']):
    # Retrieve process parameters
    build_data = np.genfromtxt('process_parameters.csv', delimiter=',', dtype=None)

    # Retrieve defect parameters
    processed_parts = []
    median_nn = []
    for f in glob.glob('*.json'):
        data = json.loads(open(f, 'rb').read())
        # Get part name and median nn
        ifile = os.path.basename(f)
        processed_parts.append(os.path.splitext(ifile)[0][:3])
        median_nn.append(data['median nearest neighbor distance']['values'])
    processed_parts = np.reshape(processed_parts, (len(processed_parts),1))
    median_nn = np.reshape(median_nn, (len(median_nn),1))

    # Identify the column (letter), row (number), and plate fields
    col_idx = np.argwhere(build_data[0,:]=='col')[0][0]
    row_idx = np.argwhere(build_data[0,:]=='row')[0][0]
    plate_idx = np.argwhere(build_data[0,:]=='plate')[0][0]
    RD_idx = np.argwhere(build_data[0,:]=='RD')[0][0]
    TD_idx = np.argwhere(build_data[0,:]=='TD')[0][0]

    # Rename the numbers in processed_parts (remove 0's)
    abbrev_parts = []
    for j in processed_parts:
        if j[0][1]=='0':
            abbrev_parts.append(j[0][0]+j[0][2])
        else:
            abbrev_parts.append(j[0])

    # Extract relevant samples only and add defect parameters
    input_data = []
    defect_data = np.concatenate((np.reshape(abbrev_parts,
                                    (len(abbrev_parts),1)),median_nn), axis=1)
    for sample in build_data:
        if any(y==sample[plate_idx] for y in plate_list):
            if (any(x==(sample[col_idx]+sample[row_idx]) for x in abbrev_parts)):
                # THIS ONLY WORKS FOR ONE PLATE ATM
                match = np.argwhere((sample[col_idx]+sample[row_idx])
                                        ==defect_data[:,0])
                sample = np.append(sample, defect_data[match,1:])
                input_data.append(sample)
    input_data = np.vstack(input_data)
    return input_data


def pca(input_data, RD_idx=18, TD_idx=19):
    # Perform a PCA/PCR on spatial parameters and defect parameters
    spatial_data = np.zeros((len(input_data), 4))
    RD, TD = input_data[:,RD_idx], input_data[:,TD_idx]
    center = [(np.max(RD)-np.min(RD))/2, (np.max(TD)-np.min(TD))/2]
    # DIVIDE BY STD
    for i in range(len(input_data)):


        spatial_data[i,:] = [input_data[i,2]+input_data[i,10],
                                input_data[i,RD_idx], input_data[i,TD_idx]],
                                ()
