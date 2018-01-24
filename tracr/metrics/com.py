from scipy.ndimage.measurements import center_of_mass

def com(arr, larr):

    """
    INPUT
    =====
        - arr (ndarray): Array of ra intensity data. Shape must match 'larr'.
        - larr (ndarray): A labeled array with 'num' clusters of integer values and '0'
                        cluster for passed material (background).

    OUTPUT
    ======
        - coms (list): An 'num+1' length list of labeled cluster centroids. This
                        includes the '0' cluster (passed signal).

    """
    num = larr.max()
    coms = center_of_mass(arr, larr, range(num+1))
    return coms
