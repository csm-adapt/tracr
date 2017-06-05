"""
Test script for TRACR Feature objects.
    - Uses generic ndarray to wrap into Feature
"""

import os, sys, glob
import numpy as np
import pytest
sys.path.append('..')
from tracr.base.feature import Feature
import warnings
warnings.simplefilter("always")


@pytest.fixture(scope="class")
def toy():
    return np.resize(np.arange(25), (5,5))

class TestToyArray:

    def test_pixel_size(self, toy):
        # Start with specified pixelsize (should raise nothing)
        px_size = 1.234
        feat = Feature(toy, pixelsize=px_size)

        # Assert object is of type Feature
        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        # Assert a 'pixelsize' attribute
        assert hasattr(feat, 'pixelsize'), \
            "Feature is missing 'pixelsize' attribute."
        # Assert pixelsize is as specified
        assert feat.pixelsize == 1.234, \
            "Actual pixelsize ({}) not match specified pixelsize ({})".format(
                feat.pixelsize, px_size)

    def test_no_pixel_size(self, toy):
        # Make sure warning is thrown without specified pixelsize
        warnings.filterwarnings("error")
        with pytest.raises(UserWarning):
            feat = Feature(toy)
        warnings.resetwarnings()

        # Above will fail, this will just give visual warnings
        feat = Feature(toy)
        # Assert object is of type Feature
        assert type(feat) is Feature, \
            'Feature is of type: {}'.format(type(feat))
        # Assert a 'pixelsize' attribute
        assert hasattr(feat, 'pixelsize'), \
            "Feature is missing 'pixelsize' attribute."
        # Assert pixelsize is as specified
        assert feat.pixelsize == 1, \
            "Actual pixelsize ({}) not match specified pixelsize ({})".format(
                feat.pixelsize, 1)
