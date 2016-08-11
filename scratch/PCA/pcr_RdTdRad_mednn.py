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


def scrape_data(plate_list=['2']):
    # Retrieve process parameters
    build_data = np.genfromtxt('process_parameters.csv', delimiter=',',
                                    dtype=None)
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
    # Identify columns of interest
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


def extract(input_data, RD_idx=18, TD_idx=19):
    ## Perform a PCA/PCR on certain spatial and defect parameters
    # Organize and normalize process parameters
    RD, TD = [np.asarray(input_data[:,RD_idx]).astype(np.float),
                    np.asarray(input_data[:,TD_idx]).astype(np.float)]

    # SHIFT TO ORIGIN
    center = 123
    radial = np.sqrt((RD-center)**2+(TD-center)**2)
    med_nn = input_data[:,-1].astype(np.float)
    RD, TD, radial, med_nn = [normalize(RD), normalize(TD), normalize(radial),
                                normalize(med_nn)]
    spatial_data = np.column_stack((RD, TD, radial, med_nn))
    np.save('RTR_mednn.npy', spatial_data)
    return spatial_data


def pcr(data):
    # Perform SVD of process parametersa
    u, s, v = np.linalg.svd(data[:,:-1], full_matrices=False)
    s = s*np.eye(len(s))
    T = np.dot(u,s)
    # Perform regression
    y = data[:,-1]
    b = np.dot(np.linalg.inv(np.dot(T.T, T)), np.dot(T.T, y))
    # Estimate error
    e = y - np.dot(T,b)
    return u, s, v, b, T, e


def normalize(iarray):
    return (iarray-np.mean(iarray))/np.std(iarray)


def wrap():
    inp = scrape_data()
    data = extract(inp)
    u, s, v, b, T, e = pcr(data)
    return u, s, v, b, T, e
