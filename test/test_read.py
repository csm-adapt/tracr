"""
Test script for TRACR file reading capability.
We want to ensure that the readers can handle the following raw data formats
and succesfully generate Feature objects from them:

TIF:
    1) SINGLE frame
    2) User specified LIST of frames (DO)
    3) MULTILAYER tif (DO)
DCM:
    1) SINGLE frame
    2) User specified LIST of frames (DO)
"""

import os, sys, glob
import numpy as np
import pytest
sys.path.append('..')
from tracr.io.read import read
from tracr.base import Feature
import warnings
warnings.simplefilter("always")

@pytest.fixture(scope="module")
def tif_frame():
    return 'testing_data/P002_B001_C04-0.4X_4.83122_0666.tif'

@pytest.fixture(scope="module")
def dcm_frame():
    return 'testing_data/P002_B001_C04-0.4X_4.83122um_.dcm0666.dcm'

@pytest.fixture(scope="module")
def hdf5_frame():
    return 'testing_data/P002_B001_Y23-0.4X_final.hdf5'

# Only using single files for now, not desirable to store huge folders
class TestReadTIF:

    def test_singleTIF(self, tif_frame):
        # No pixel size here
        feat = read(tif_frame)
        # Make assertions, tests, etc.
        assert isinstance(feat, Feature), \
            'Feature is of type: {}'.format(type(feat))
        assert np.sum(feat) == 9953421973, \
            'Checksum of Feature is: {} ' \
            '(should be 9953421973)'.format(np.sum(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 1.0, 'Pixelsize not set to 1'

    # Insert multilayer tif reading tests:

    # Insert list of frames tests:


class TestReadDCM:
    def test_singleDCM(self, dcm_frame):
        # No pixel size here
        feat = read(dcm_frame)
        # Make assertions, tests, etc.
        assert isinstance(feat, Feature), \
            'Feature is of type: {}'.format(type(feat))
        assert np.sum(feat) == 9953421973, \
            'Checksum of Feature is: {} ' \
            '(should be 9953421973)'.format(np.sum(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 4.831, 'Pixel size not set to 1'


class TestReadHDF5:
    def test_hdf5(self, hdf5_frame):
        # No pixel size here
        feat = read(hdf5_frame)
        # Make assertions, tests, etc.
        assert isinstance(feat, Feature), \
            'Feature is of type: {}'.format(type(feat))
        assert hasattr(feat, 'pixelsize'), 'No pixelsize attribute'
        assert feat.pixelsize == 4.8920965127763338, "Wrong pixel size"
