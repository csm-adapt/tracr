"""
Test script for TRACR file reading capability.
FOR NOW: Running test on 2D sample, will scale up to data shortly
"""

import os, sys, glob
sys.path.append('..')
from tracr.io.tif.read import read_single as read_singleTIF
from tracr.io.tif.read import read_multilayer as read_multiTIF

class TestReadTIF:

    def test_singleTIF(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122_0666.tif'
        arr = read_singleTIF(data)
        # Make assertions, tests, etc.

    # Insert multilayer tif reading tests

    # Insert tif folder tests


    # Insert *any* tif tests (for tracr.io.tif.read function)


class TestReadDCM:

    # Insert single dcm reading tests (testing tracr.io.dcm.read)

    # Insert dcm folder reading tests

class TestReadANY:
    # Insert test for either tif or dcm (testing tracr.io.read)
