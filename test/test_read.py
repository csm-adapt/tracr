"""
Test script for TRACR file reading capability.
FOR NOW: Running test on 2D sample, will scale up to data shortly
"""

import os, sys, glob
sys.path.append('..')
from tracr.io.tif import read as readTIF
from tracr.io.dcm import read as readDCM
from matplotlib import pyplot as plt

# Only using single files for now, not desirable to store huge folders
class TestReadTIF:

    def test_singleTIF(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122_0666.tif'
        feat = readTIF(data)

        # Make assertions, tests, etc.
        assert type(feat) is Feature
        print feat.nlabels
        plt.figure()
        plt.imshow(feat.labels)
    # Insert multilayer tif reading tests

    # Insert tif folder tests


    # Insert *any* tif tests (for tracr.io.tif.read function)


class TestReadDCM:
    def test_singleDCM(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122um_.dcm0666.dcm'
        feat = readDCM(data)

        # Make assertions, tests, etc.
        assert type(feat) is Feature
        print feat.nlabels
        plt.figure()
        plt.imshow(feat.labels)


    # Insert single dcm reading tests (testing tracr.io.dcm.read)

    # Insert dcm folder reading tests
