from scipy.ndimage.measurements import center_of_mass


def com(mask):
    """
    Finds the center of mass of the object defined by MASK.
    """
    return np.mean(np.where(mask).T, axis=0)


def pore_com(porosity):
    # your masterful COM code
    return center_of_mass(porosity.array, porosity.labels)
