"""
Test script for TRACR file reading capability.
FOR NOW: Running test on 2D sample, will scale up to data shortly
"""

import os, sys, glob
sys.path.append('..')
from tracr.io.read import read
from tracr.io.tif import read as readTIF
from tracr.io.dcm import read as readDCM
from matplotlib import pyplot as plt

# Only using single files for now, not desirable to store huge folders
class TestReadTIF:
    # Do not specify pixel size
    def test_singleTIF(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122_0666.tif'
        feat = read(data)

        # Make assertions, tests, etc.
        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        assert np.sum(feat) == 9953421973, \
            'Checksum of Feature is: {} ' \
            '(should be 9953421973)'.format(np.sum(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 1.0, 'Pixelsize not set to 1'

    # Specify pixel size
    def test_singleTIF_px(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122_0666.tif'
        feat = read(data, pixelsize=4.5)

        # Make assertions, tests, etc.
        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        assert np.sum(feat) == 9953421973, \
            'Checksum of Feature is: {} ' \
            '(should be 9953421973)'.format(np.sum(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 4.5, 'Pixelsize not as specified'


    # Insert multilayer tif reading tests:


class TestReadDCM:
    def test_singleDCM(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122um_.dcm0666.dcm'
        feat = readALL(data)

        # Make assertions, tests, etc.
        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        assert np.sum(feat) == 9953421973, \
            'Checksum of Feature is: {} ' \
            '(should be 9953421973)'.format(np.sum(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 1.0, 'Pixel size not set to 1'

    def test_singleDCM_px(self):
        data = 'testing_data/P002_B001_C04-0.4X_4.83122um_.dcm0666.dcm'
        feat = readALL(data, pixelsize=4.5)

        # Make assertions, tests, etc.
        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        assert np.sum(feat) == 9953421973, \
            'Checksum of Feature is: {} ' \
            '(should be 9953421973)'.format(np.sum(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 4.5, 'Pixel size not as specified'


    # Insert single dcm reading tests (testing tracr.io.dcm.read)

    # Insert dcm folder reading tests
