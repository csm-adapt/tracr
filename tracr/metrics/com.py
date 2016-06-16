from scipy.ndimage.measurements import center_of_mass
from ..structures import Porosity


def com(obj):
    """
    Finds the center of mass of the object defined by OBJ.
    """
    # check for optimized implementations
    if isinstance(obj, Porosity):
        return pore_com(obj)
    else:
        # fall back on a default
        return np.mean(np.where(mask).T, axis=0)


def pore_com(porosity):
    # your masterful COM code
    return center_of_mass(porosity.array, porosity.labels)
