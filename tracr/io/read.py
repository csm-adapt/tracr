# tries to guess the format of the file
from .util import guess_format, check_format
from .tif import read as read_tif

def read(filename, **kwds):
    fmt = kwds.get('format', guess_format(filename))
    fmt = check_format(fmt)
    if fmt == 'tif':
        return read_tif(filename)
    else:
        raise RuntimeError('You should never get here!')
