
# coding: utf-8

# In[61]:

#!/usr/bin/env python

"""
DESCRIPTION

    Script for scraping process parameters and defect parameters for PCA
    Outfitted for use with 'process_parameters.csv'
"""

from __future__ import division
from scipy import stats
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys, os, glob
import numpy as np
import json

def scrape_data(all_build_data=None, plate_list=['2'],
                 feat_list=None, resp_var=None, stat_param=None):

    # Retrieve all build features
    if all_build_data==None:
        try:
            all_build_data = np.genfromtxt('process_parameters.csv', delimiter=',',
                                             dtype=None)
        except IOError:
            print 'Please input a process_parameters file'

    # Obtain build features of interest
    if feat_list==None:
        print 'Please input a feature list with keys matching p_p file'
    idx = {}
    idx['plate'] = np.argwhere(all_build_data[0,:]=='plate')[0][0]
    for feat in feat_list:
        idx[feat] = np.argwhere(all_build_data[0,:]==feat)[0][0]

     # Obtain user specified defect parameter for regression
    if resp_var==None:
        print json.loads(open('A13_pore-distribution.json', 'rb').read()).keys()
        resp_var = raw_input('Please enter (void specific) response variable: ')
    if stat_param==None:
        stat_param = raw_input("Please enter statistical metric (mean, median, mode): ")

    # Iterate through .json files for response parameters
    processed_parts = []
    response = []
    for f in glob.glob('*.json'):
        data = json.loads(open(f, 'rb').read())
        ifile = os.path.basename(f)
        processed_parts.append(os.path.splitext(ifile)[0][:3])
        if stat_param=='mean':
            response.append(np.mean(data[resp_var]['values']))
        elif stat_param=='mode':
            response.append(stats.mode(part[resp_var]['values'],axis=None)[0][0])
        else:
            response.append(np.median(data[resp_var]['values']))
    np.reshape(processed_parts, (len(processed_parts),1))
    np.reshape(response, (len(response),1))

    # Remove zeros from part names in 'processed_parts'
    abbrev_parts = []
    for j in processed_parts:
        if j[1]=='0':
            abbrev_parts.append(j[0]+j[2])
        else:
            abbrev_parts.append(j)
    np.reshape(abbrev_parts,(len(abbrev_parts),1))

    # Generate ID-response array
    input_data = []
    ID_response = np.vstack((np.asarray(abbrev_parts).T, np.asarray(response).T)).T
    for sample in all_build_data:
        if any(y==sample[idx['plate']] for y in plate_list):
            if (any(x==(sample[idx['col']]+sample[idx['row']]) for x in abbrev_parts)):
                match = np.argwhere((sample[idx['col']]+sample[idx['row']])==
                                        ID_response[:,0])
                sample = np.append(sample, ID_response[match,1:])
                input_data.append(sample)
        input_data = np.vstack(input_data)
    return input_data

def pcr(all_build_data=None, plate_list=['2'], feat_list=None, resp_var=None,
         stat_param=None):
    # Perform an SVD of the build data
    data = scrape_data(all_build_data=None, plate_list=['2'], feat_list=None,
                        resp_var=None, stat_param=None)
    u, s, v = np.linalg.svd(data[:, :-1], full_matrices=False)
    s = np.diag(s)
    T = np.dot(u,s)

    # Incorporate response variable for regression
    y = data[:,-1]
    b = np.dot(np.linalg.inv(np.dot(T.T, T)), np.dot(T.T, y))

    # Error approximation
    e = y - np.dot(T, b)

def normalize(iarray):
    return (iarray - np.mean(iarray)).np.std(iarray)
