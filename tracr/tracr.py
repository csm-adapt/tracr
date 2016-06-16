#!/usr/bin/env python
"""
DESCRIPTION

    Tomography Reconstruction Analysis and Characterization Routines
    is used to process tomography data.

EXAMPLES

    TODO: Show some examples of how to use this script.
"""

from __future__ import division

# ###########################
# ensure tracr is in the path
import sys,os
# get the parent directory of the directory that contains this file
# having resolved all symbolic links, etc. so it points to the original
# file.
parent, child = os.path.split(os.path.split(os.path.realpath(__file__))[0])
# prepend the parent directory to the path
sys.path = [parent] + sys.path
# ###########################

from tracr.structures import Porosity
from tracr.actions import ExternalThreshold
from tracr.io import read, write
from tracr.metrics.com import pore_com
from tracr.metrics.volume import pore_volume

import sys, os, textwrap, traceback, argparse
import time
import shutil
#from pexpect import run, spawn


def threshold(*positional, **named):
    """
    Identifies and applies a threshold to images in order to distinguish
    porosity (low attenuating volumes) from solid (high attenuating volumes).
    """
    # args is the global args variable. This is not declared "global args"
    # because these are immutable in threshold.
    matlab = getattr(args, 'matlab',
                     '/Applications/MATLAB_R2015b.app/bin/matlab')
    cmd = ' '.join([
        '-nosplash ',
        '-nodesktop',
        '-r "run(\'{}/bin/Thresholding/imageThresholding.m\'); ' \
            'exit()";'.format(parent)])
    action = ExternalThreshold(matlab, parameters=[cmd])
    return action()


def centers_of_mass(filename, **kwds):
    """
    Calculates the centers of mass of the pores in FILENAME.
    """
    # reads in the tif
    arr = read(filename)
    # determine pore locations
    pores = Porosity(arr)
    # call your COM code
    com = pore_com(pores)
    # TODO: write a csv writer
    write(args.ofile, com)
#def com(*filenames):

def volumes(filename, **kwds):
    """
    Calculates the volumes of the pores in FILENAME.
    """
    # reads in the tif
    arr = read(filename)
    # determine pore locations
    pores = Porosity(arr)
    # call your COM code
    vol = pore_volume(pores)
    # TODO: write a csv writer
    write(args.ofile, vol)
#def com(*filenames):


def main ():
    global args
    # execute the requested action with required positional arguments
    args.action(*getattr(args, 'positional', []))
#end 'def main ():'

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(
                #prog='HELLOWORLD', # default: sys.argv[0], uncomment to customize
                description=textwrap.dedent(globals()['__doc__']),
                epilog=textwrap.dedent("""\
                    EXIT STATUS

                        0 on success

                    AUTHOR

                        Branden Kappes <bkappes@mines.edu>

                    LICENSE

                        This script is in the public domain, free from copyrights
                        or restrictions.
                        """))
        # top level parser
        # optional parameters
        parser.add_argument('-v',
            '--verbose',
            action='count',
            default=0,
            help='Verbose output')
        parser.add_argument('--version',
            action='version',
            version='%(prog)s 0.1')
        # subparsers
        subparsers = parser.add_subparsers(
            help='sub-command help')
        #
        # threshold parser
        subparser_threshold = subparsers.add_parser('threshold',
            help='Threshold images to differentiate porosity (low ' \
                 'attenuation) and solid (high attenuation) volumes.')
        # positional parameters
        # parser.add_argument('filelist',
        #     metavar='file',
        #     dest='positional',
        #     type=str,
        #     nargs=*, # if there are no other positional parameters
        #     nargs=argparse.REMAINDER, # if there are
        #     help='Files to process.')
        subparser_threshold.set_defaults(
            positional=[],
            action=threshold)
        #
        # center of mass
        subparser_com = subparsers.add_parser('com',
            help='Calculates the centers of mass for all voids in an image ' \
                 'or collection of images.')
        # positional parameters
        subparser_com.add_argument('filenames',
            metavar='file',
            dest='positional', # if different than the name of the argument
            type=str,
            nargs='*', # if there are no other positional parameters
            #nargs=argparse.REMAINDER, # if there are
            help='Files to process.')
        subparser_com.add_argument('-o',
            '--output',
            dest='ofile',
            default='pore_com.csv'
            help='Set the output filename for the COM calculation (CSV file).')
        subparser_threshold.set_defaults(
            positional=[],
            action=centers_of_mass)
        #
        # void volumes
        subparser_volume = subparsers.add_parser('volume',
            help='Calculates the volumes for all voids in an image ' \
                 'or collection of images.')
        # positional parameters
        subparser_volume.add_argument('filenames',
            metavar='file',
            dest='positional', # if different than the name of the argument
            type=str,
            nargs='*', # if there are no other positional parameters
            #nargs=argparse.REMAINDER, # if there are
            help='Files to process.')
        subparser_volume.add_argument('-o',
            '--output',
            dest='ofile',
            default='pore_volume.csv'
            help='Set the output filename for the volume calculation (CSV file).')
        subparser_threshold.set_defaults(
            positional=[],
            action=volumes)
        args = parser.parse_args()
        # check for correct number of positional parameters
        #if len(args.filelist) < 1:
            #parser.error('missing argument')
        # timing
        if args.verbose > 0: print time.asctime()
        main()
        if args.verbose > 0: print time.asctime()
        if args.verbose:
            delta_time = time.time() - start_time
            hh = int(delta_time/3600.); delta_time -= float(hh)*3600.
            mm = int(delta_time/60.); delta_time -= float(mm)*60.
            ss = delta_time
            print 'TOTAL TIME: {0:02d}:{1:02d}:{2:06.3f}'.format(hh,mm,ss)
        sys.exit(0)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)
#end 'if __name__ == '__main__':'
