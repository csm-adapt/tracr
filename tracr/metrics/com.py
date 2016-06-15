from scipy.ndimage.measurements import center_of_mass

def pore_com(porosity):
    # your masterful COM code
    return center_of_mass(porosity.array, porosity.labels) 
