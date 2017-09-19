from scipy.ndimage.measurements import label

"""
Calculates the labeled array from a binarized array. Any cluster of '1' valued
clusters is uniquely enumerated while the background '0' is kept the same.

Input
=====
: arr (boolean array): array of binarized intensity data after thresholding.

Output
=====
: lbl (ndarray): array of uniquely enumerated 'True' clusters.
"""

def label(arr, *args):
    lbl, num = label(arr)
    return lbl
