"""
File reading tools for decomposing input file name. Returns format string
depending on extension (either '.tif/.tiff' or '.dcm/.dicom').

INPUT:
    - string containing file name (presumably not folder due to ./read.py)

OUTPUT:
    - string declaring extension (tif or dcm)
"""

import os

def guess_format(filename):
    # Guess the format of the file
    pathstr, basename = os.path.split(filename)
    name, ext = os.path.splitext(basename)
    ext = ext.lower()
    # List recognized filenames
    if ext in ('.tif', '.tiff'):
        return 'tif'
    elif ext in ('.dcm', '.dicom'):
        return 'dcm'
    else:
        msg = 'Could not guess the format of {}.'.format(filename)
        raise IOError(msg)


# What is the point of this?
# def check_format(fmt):
#     fmt = fmt.lower()
#     if ext in ('tif', 'tiff'):
#         return 'tif'
#     elif ext in ('dcm', 'DCM')
#         return 'dcm'
#     else:
#         msg = '{} format is not a recognized format.'.format(fmt)
#         raise IOError(msg)

