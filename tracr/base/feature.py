"""
Generation of our 'Feature' object. This class accepts a numpy array of the
raw intensity data (read in from tracr.io.read). It extends the ndarray class
by further attributing: label count, volumes, COMs, etc.
"""
# Will add more thresholding schemes once we clean up thresholding functions:
import numpy as np
import logging
from warnings import warn
logging.basicConfig(filename='feature.log', level=logging.DEBUG)

class Feature(np.ndarray):
    # Where 'object' represents the numpy array of pre-read intensity data
    # create a new Feature object as a view
    def __new__(cls, arr, **kwds):
        #self.set_array(arr, **kwds)
        obj = np.asarray(arr).view(cls)

        # Check for pixel size
        if 'pixelsize' not in kwds:
            msg = "'pixelsize' was not set when Feature object was created. " \
                "A pixel size of 1 is assumed for all calculations (pixel dim's)."
            warn(msg)

        # Record pixelsize in log file
        obj.pixelsize = kwds.get('pixelsize', 1)
        logging.info("Pixel size: {} um".format(obj.pixelsize))
        return obj

    def __array_finalize__(self, obj):

        # when creating a new instance, this is called before the
        # instance is actually created (i.e. when `__new__` is called)
        if obj is None:
            return
        #self.pixelsize = getattr(obj, 'pixelsize', 1)
