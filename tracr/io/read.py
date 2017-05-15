# tries to guess the format of the file
"""
Read in TIF or DCM intensity data and send to appropriate reader depending on
format. If keyword arg specified for 'format', this is just a wrapper for the
readers. If not, we guess. So far, this assumes that a folder input contains
data frames directly below (i.e. there are no nested folders.) and that
contained files are listed sequentially. Unspecified pixel size is set to 1.

INPUT:
    - TIF: file (single or multilayer), or user specified list of frames
    - DICOM: file (single), or list of dcm frames

OUTPUT:
    - Feature object of intensity data. See specific readers for more.

USAGE:
    e.g. read(glob.glob('myDataFolder/*tif'))
    e.g. read('path/to/sampleX.dcm', format='dcm'), (no guessing here)
    e.g. read('path/to/sampleX.tif', pixelsize=4.5)
"""

import os, glob
from .util import guess_format
from .tif import read as read_tif
from .dcm import read as read_dcm

def read(filename, **kwds):
    # If format specified, great (still lower it). If not, we call guesser.

    # Check if input is iterable (e.g. list of files sent by user)
    # Note: os.path.isfile(iterable) throws error so this comes in the 'if'
    if hasattr(filename, '__iter__'):
        fmt = kwds.get('format', guess_format(filename[0]))
    # If not, input is a single frame or multialyer file
    else:
        fmt = kwds.get('format', guess_format(filename))

    # Check for pixel size keyword. Set to '1' if unspecified. This will log
    # in Feature.
    px_size = kwds.get('pixelsize', 1)

    # Select appropriate reader based on 'fmt' - they will check if file/folder
    if fmt.lower() in ('tif', 'tiff'):
        return read_tif(filename, pixelsize=px_size)
    elif fmt.lower() in ('dcm', 'dicom'):
        return read_dcm(filename, pixelsize=px_size)
    else:
        msg = '{} is not a recognized input format.'.format(fmt)
        raise NotImplementedError(msg)

if __name__ == '__main__':
    try:
        # Load inputs and read ifile normally
        ifile = sys.argv[1]
        path, base = os.path.split(ifile)
        intensity_array = read(ifile)
        try:
            ofile = sys.argv[2]
        except IndexError:
            # Extract path for saving array
            ofile, ext = os.path.splitext(base)
        np.save(path+'_'+ofile, intensity_array)
    except IndexError:
		sys.stderr.write('CL Usage: python {} [path/to/ifile] [ofile_name]'.format(sys.argv[0]))
		sys.exit(1)
