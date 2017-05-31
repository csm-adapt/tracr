"""
Test script for TRACR Feature objects.
FOR NOW: Testing type and pixelsize attribute
"""

import os, sys, glob
import numpy as np
sys.path.append('..')
from tracr.base.feature import Feature
from tracr.io.read import read

class TestFeature:

    def test_toy_array(self):
        # Start with specified pixelsize (should raise nothing)
        frame = np.resize(np.arange(25), (5,5))
        feat = Feature(frame, pixelsize=1.234)

        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        # figure out asseriton for NOT raising log warning (testfixtures??)

        # Try new frame without pizelsize
        feat2 = Feature(frame)

        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        # Assert that warning WAS RAISED

    def test_XCT_layer(self):
        # Read already expected to return a Feature object, how to send px size?
        feat = read('testing_data/P002_B001_C04-0.4X_4.83122_0666.tif')

        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
