#!/usr/bin/env python
"""
DESCRIPTION

    Tomography Reconstruction Analysis and Characterization Routines
    is used to process tomography data.

EXAMPLES

    TODO: Show some examples of how to use this script.
"""

from tracr.actions import ExternalThreshold
import sys, os, textwrap, traceback, argparse
import time
import shutil
#from pexpect import run, spawn


def threshold(*args):
    action = ExternalThreshold('matlab',
        parameters=['../bin/Thresholding/imageThresholding.m'])
    return action()


def main ():
    global args

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
