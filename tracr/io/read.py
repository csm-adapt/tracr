# tries to guess the format of the file
"""
Read in TIF or DCM intensity data and send to appropriate reader depending on
format. Assume that a folder input contains data frames directly below
(i.e. there are no nested folders.)

INPUT:
    - TIF: file (single or multilayer), or folder of TIF frames
    - DICOM: file (single), or folder of DCM frames

OUTPUT:
    - Numpy array of intensity data. See specific readers for more.

USAGE:
    e.g. read('path/to/DataFolder/')
    e.g. read('path/to/sampleX.dcm')
    e.g. read('path/to/sampleX.tif')
"""


from .util import guess_format, check_format
from .tif import read as read_tif
from .dcm import read as read_dcm

def read(filename, **kwds):
    # Not sure what keywords we would pass here...
    #fmt = kwds.get('format', guess_format(filename))
    #fmt = check_format(fmt)

    ## Check if user input is a file or folder of files
    if os.path.isdir(filename):
        fmt = guess_format(os.listdir(filename)[0])
    else:
        fmt = guess_format(filename)
    # Select appropriate reader
    if fmt == 'tif':
        return read_tif(filename)
    elif fmt == 'dcm':
        return read_dcm(filename)
    else:
        msg = '{} is not a recognized input format.'.format(fmt)
        raise NotImplementedError(msg)
