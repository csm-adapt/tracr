"""
File reading tools for decomposing input file name. Returns format string
depending on extension (either '.tif/.tiff' or '.dcm/.dicom').

INPUT:
    - string containing file name. If folder, we access first file.

OUTPUT:
    - string declaring extension (tif or dcm)
"""

import os

def guess_format(filename):
    # Check if input is directory or not. If so, grab first file within.
    if os.path.isdir(filename):
        pathstr, basename = os.path.split(filename[0])
    else:
        pathstr, basename = os.path.split(filename)
    # Guess the format of the file
    name, ext = os.path.splitext(basename)
    ext = ext.lower()
    # list recognized filenames
    if ext in ('.tif', '.tiff'):
        return 'tif'
    elif ext in ('.dcm', '.dicom')
        return 'dcm'
    else:
        msg = 'Could not guess the format of {}.'.format(filename)
        raise IOError(msg)
