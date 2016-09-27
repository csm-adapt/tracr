# coding: utf-8

# In[101]:

import sys, os
sys.path.append('/home/hgeerlings/src/tracr/')


# In[102]:

from time import time
from tracr.actions.threshold import otsu
from tracr.io.tif import read_single
from pixel_sizes import pixel_dict
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from PIL import Image
from scipy.ndimage.measurements import label, center_of_mass
from scipy.spatial import cKDTree
import json
import glob
from joblib import Parallel, delayed


# Read a sample
def read_sample(stack):
    return np.array([read_single(frame) for frame in stack])


# Segment the sample
def segment_sample(arr):
    threshold = otsu(arr)
    mask = (arr < threshold)
    return (threshold, label(mask, structure=np.ones((3,3,3))))


# Calculate volume of each pore
def pore_volumes(seg):
    """Returns the volume of the pore (in microns)"""
    larr, num = seg
    num = larr.max()
    vols = np.zeros(num+1)
    np.add.at(vols, larr.flat, 1)
    return vols[1:]


# Calculate COM of each pore
def pore_COMs_generator(tomo):
    def func(seg):
        larr, num = seg
        coms = np.array(center_of_mass(tomo, larr, range(1, num+1)))
        return coms
    return func


# Calculate nearest neighbor distances
def nearest_neighbors(poreCOM, tree=None):
    # use tracr to determine NN distance
    if tree is None:
        tree = cKDTree(poreCOM)
    # search for two nearest neighbors: the first will always be
    # itself, the second will be an actual neighbor. query returns
    # [(d1, d2), (i1, i2)], return these as distance/neighbor pairings
    process = lambda d,i: (d, poreCOM[i])
    nn = [process(*zip(*tree.query(x, k=2))[1]) for x in poreCOM]
    return nn


# Calculate median pore spacing
def median_spacing(nnlist):
    """Returns the median from a list of nearest neighbor info."""
    return np.median([nn[0] for nn in nnlist])


def strtime(sec):
    mm = int(sec // 60)
    ss = sec - 60*mm
    return "{:02d}:{:.3f}".format(mm, ss)

def process_tif_directory(name, stack, skip_existing=True):
    """Sequence of steps required to analyze a single directory."""
    #print name
    start = time()
    # IN FUTURE VERSIONS, CLEAN THIS UP!
    # This function wraps read-process-write into a single function!
    ofile = '{}-porosity.json'
    if skip_existing:
        try:
            # if the file exists, do not process this file
            open(ofile).close()
            return
        except IOError:
            pass
    try:
        # Read the tif series and convert to 3D array
        tomo = read_sample(stack)
        # Threshold the 3D array
        threshold, seg = segment_sample(tomo)
        # Load the voxel sizes
        px_dict = pixel_dict()
        px = px_dict[name[:3]]
        # Calculate void volumes
        volumes = px**3 * pore_volumes(seg)
        # COMs
        pore_COMs = pore_COMs_generator(tomo)
        coms = px * pore_COMs(seg)
        # Find nn list for each void
        nn = nearest_neighbors(coms)
        # Find median nn spacing
        mps = median_spacing(nn)
        # Save histograms
        plt.hist(tomo.flatten(), bins=256, log=True)
        plt.axvline(threshold, color='r')
        plt.savefig("{}-hist.png".format(name))
        # Save results
        result = {
            'volume' : volumes.tolist(),
            'center of mass' : coms.tolist(),
            'neighbors' : [n[0] for n in nn],
            'median pore spacing' : mps
        }
        # write the results as a JSON file
        with open('{}-porosity.json'.format(name), 'w') as fp:
            json.dump(result, fp)
        stop = time()
        print "Processed {file:} in {time:}".format(file=name, time=(stop-start))
    except:
        stop = time()
        print "Error occured while processing {file:}.".format(file=name)

def main():
    # Generate the list of files
    samples = [sample.strip('inconel/')
               for sample in glob.glob('inconel/[A-Y][0-9][0-9]*')]
    tifs = dict([(sample,
                  sorted(glob.glob('inconel/{}/Multi*/*.tif*'.format(sample))))
                 for sample in samples])
    # eliminate empty directories
    for k,v in iter(tifs.items()):
        if len(v) == 0:
            del tifs[k]
    # process tif directories
    # Parallel version
    Parallel(n_jobs=5)(delayed(process_tif_directory)(name, stack)
        for name, stack in iter(tifs.items()))
    # Serial version
    # for name, stack in iter(tifs.items()[:1]):
    #     process_tif_directory(name, stack)

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
        # positional parameters
        #parser.add_argument('filelist',
            #metavar='file',
            #type=str,
            #nargs='*', # if there are no other positional parameters
            #nargs=argparse.REMAINDER, # if there are
            #help='Files to process.')
        # optional parameters
        parser.add_argument('-v',
            '--verbose',
            action='count',
            default=0,
            help='Verbose output')
        parser.add_argument('--version',
            action='version',
            version='%(prog)s 0.1')
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
