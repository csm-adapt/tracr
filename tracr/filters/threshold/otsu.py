import numpy as np
from itertools import combinations
from .threshold import register_threshold
from skimage.filters import threshold_otsu as skimage_otsu

@register_threshold
def tracr_otsu(image, nclasses=2, nbins=256, *args): # otsu implementation
    """
    Calculates the threshold levels for an image using the multilevel
    otsu implementation from Deng-Yuan Huang and Chia-Hung Wang,
    "Optimal multi-level thresholding using a two-stage Otsu optimization
    approach", Pattern Recognition Letters 30 (2009) 275-284,
    doi:10.1016/j.patrec.2008.10.003.

    This is an implementation of the recursive algorithm (lookup table)
    from Liao (2001), and referenced by Huang and Wang.

    Input
    -----
    :image, array-like: Image intensity data
    :nclasses, int: (optional) Number of classes into which the data should
        be subdivided. Default: 2 (two classes --> one threshold)
    :nbins, int: (optional) A histogram of *nbins* will be made from the
        intensity values in *image*. This provides the number of bins in
        that histogram. Default: 256
    :'trim', (optional) ignores nonzero entries of dataset


    Output
    ------
    Threshold levels (tuple)
    """
    # ensure the image is a numpy array-like
    image = np.asarray(image)
    # trim off zero intensities (usually in frame corners) if desired
    if 'trim' in args:
        image = image[np.nonzero(image)]
    # calculate the histogram of intensities
    prob, edges = np.histogram(image.flatten(), bins=nbins, density=True)
    nbins = len(prob)
    # H-table (and similarly P-table and S-table from which H-table
    # is derived) is a lookup table where the start point is the first
    # index and the end point is the second index, i.e.
    #   `htable[12, 27]`
    # holds the modified variance of the class in the range [12, 27)
    triu = np.triu(np.ones((nbins, nbins)))
    # calculate the P-table
    ptable = np.concatenate([
        np.expand_dims(np.dot(triu[:,:threshold], prob[:threshold]), axis=1)
        for threshold in xrange(1, nbins+1)], axis=1)
    # calculate the S-table
    stable = np.concatenate([
        np.expand_dims(np.dot(triu[:,:threshold],
                       np.arange(threshold)*prob[:threshold]), axis=1)
        for threshold in xrange(1, nbins+1)], axis=1)
    # calculate the H-table
    olderr = np.seterr(divide='ignore')
    htable = stable**2/ptable
    np.seterr(**olderr)
    # find the thresholds that maximize the interclass variance
    nthresh = nclasses-1
    max_variance = 0
    for ijk in combinations(xrange(1, nbins-1), nthresh):
        ijk = (0,) + ijk + (-1,) # append the start and end points
        variance = sum([htable[i,j] for i,j in zip(ijk[:-1], ijk[1:])])
        if variance > max_variance:
            max_variance = variance
            thresholds = tuple((edges[i] + edges[i+1])/2.
                               for i in ijk[1:-1])
    return thresholds


@register_threshold
def otsu(*args, **kwds):
    """Otsu wrapper..."""
    method = {
        'skimage' : skimage_otsu,
        'tracr' : tracr_otsu
    }.get(
        kwds.get('method', tracr_otsu),
        kwds.get('method', tracr_otsu))
    if 'method' in kwds:
        del kwds['method']
    return method(*args, **kwds)
