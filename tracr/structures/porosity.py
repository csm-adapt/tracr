from scipy.ndimage.measurements import label

class Porosity(object):
    """
    Accepts a 3D intensity array and determines the pore/void
    locations.
    """
    def __init__(self, arr, *args, **kwds):
        """
        Create a porosity object from a mask of the void space, where
        non-zero values represent the empty space and zero values represent
        the non-empty space.

        Examples:

            mask = (image_array < threshold)
            porosity = Porosity(mask, exclude='largest')

        Parameters
        ----------
        :arr, array-like: Typically a boolean mask that defines what objects
            represent the void space.

        Keywords
        --------
        :exclude, keyword string: Exclude some volume, e.g. air. Recognized
            strings: 'largest' = largest volume
        """
        # intensity array
        self.set_array(arr, **kwds)
        # the mask will often include air/environment -- optionally exlude this
        if kwds.get('exclude', None) == 'largest':
            self.exclude_largest()

    def __iter__(self):
        for ilab in xrange(1, self.nlabels+1):
            yield (self.labels == ilab)

    def set_array(self, arr, **kwds):
        kwds['structure'] = kwds.get('structure', np.ones((3,3,3)))
        self._structure = kwds['structure'] # keep record of this
        self._arr = np.asarray(arr)
        labels, num = label(self._arr, **kwds)
        self._labels = labels
        self._nlabels = num

    def exclude_largest(self):
        """
        This eliminates the ambient air 'pore'
        """
        mask = np.copy(self.array)
        vols = [np.sum(p) for p in self]
        ilarge = np.argmax(vols)+1 # pore types are 1-indexed
        mask[self.labels == ilarge] = 0
        self.set_array(mask, structure=self._structure)

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
