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

import os
import logging
logging.basicConfig(filename='feature.log', level=logging.DEBUG)
from .util import guess_format
from .tif import read as read_tif
from .dcm import read as read_dcm

def read(ifile, **kwds):
    # Determine whether input is file or list of files, and ensure output is list
    try:
        # Turn single file (single or multilayer) into a list
        if os.path.isfile(ifile):
            filenames = [ifile]
    except TypeError:
        # Input is a user-specified list of frames
        if hasattr(ifile, '__iter__'):
            filenames = ifile
        else:
            raise

    # Collect and check for mixed file types in list
    formats = [kwds.get('format', guess_format(f)) for f in filenames]
    num_formats = len(list(set(formats)))
    if num_formats != 1:
        # Only print first list item to prevent explosion
        msg = 'More than one file format found in {}'.format(filenames[0])
        raise IOError(msg)

    # Check for specified pixelsize, warn if not specified.
    try:
        px_size = kwds['pixelsize']
    except KeyError:
        msg = 'Pixel size was not specified and is not provided in {}. ' \
                'Default to 1.'.format(filenames[0])
        print msg
        px_size = 1.0

    # Select appropriate reader based on 'fmt' - they will check if file/folder.
    # 'pixelsize' is a set **kwds argument from here on out.
    if fmt.lower() in ('tif', 'tiff'):
        return read_tif(filenames, pixelsize=px_size)
    elif fmt.lower() in ('dcm', 'dicom'):
        return read_dcm(filenames, pixelsize=px_size)
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
