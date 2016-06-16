from scipy.ndimage.measurements import label

class Porosity(object)
    """
    Accepts a 3D intensity array and determines the pore/void
    locations.
    """
    def __init__(self, arr, *args, **kwds):
        # intensity array
        self.set_array(arr)

    def __iter__(self):
        for ilab in xrange(1, self.nlabels+1):
            yield (self.labels == ilab)

    def set_array(self, arr, **kwds):
        kwds['structure'] = kwds.get('structure', np.ones((3,3,3)))
        self._arr = np.asarray(arr)
        labels, num = label(self._arr, **kwds)
        self._labels = labels
        self._nlabels = num

    @property
    def array(self):
        return self._arr

    @property
    def labels(self):
        return self._labels

    @property
    def nlabels(self):
        return self._nlabels
#end 'class Pore(object)'
