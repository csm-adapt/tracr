"""
Generation of our 'Feature' object. This class accepts a numpy array of the
raw intensity data (read in from tracr.io.read). It extends the ndarray class
by further attributing: label count, volumes, COMs, etc.
"""
# Will add more thresholding schemes once we clean up thresholding functions:
from skimage.filters import threshold_otsu as skotsu
from scipy.ndimage.measurements import label, center_of_mass

class Feature(object):
    # Where 'object' represents the numpy array of pre-read intensity data
    # This object is initiated within tracr.io.read
    def __init__(cls, arr, **kwds):
        #self.set_array(arr, **kwds)
        obj = np.asarray(arr).view(cls)

        # Check for pixel size
        obj.pixelsize = kwds.get('pixelsize', None)
        return obj

    #def set_array(self, arr, **kwds):
        #self.thresh_val = self.threshold(arr)
        #self.labels, self.nlabels = label((arr < self.thresh_val))

    #def threshold(self, arr):
        #return skotsu(arr.flatten())
