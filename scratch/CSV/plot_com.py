#!/usr/bin/env python
#
# Plots the COM of a void on the slice that contains that COM
#

import os, sys
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image, ImageSequence
try:
    from pixel_sizes import pixel_dict
except ImportError:
    pixel_dict = lambda : {}
from scipy.ndimage.measurements import label


def plot_com(filename):
    # read .tif
    print('Loading image')
    tiffile = filename
    path, filename = os.path.split(filename)
    path = '.' if path == '' else path
    prefix, ext = os.path.splitext(filename)
    img = Image.open(tiffile)
    csv = np.loadtxt('{}/{}.csv'.format(path, prefix), delimiter=',')
    # convert to array
    print('Converting to array')
    arr = np.array([np.array(frame) for frame in ImageSequence.Iterator(img)])
    arr = np.transpose(arr, axes=(1,2,0))
    # convert um to pixels
    try:
        micronsPerPixel = pixel_dict()[prefix]
    except KeyError:
        micronsPerPixel = float(raw_input('How many microns per pixel? '))
    um2pix = lambda x : x/micronsPerPixel
    pix2um = lambda x : micronsPerPixel*x
    csv[:,1:4] = um2pix(csv[:,1:4]) # for COM locations only
    print('Finding voids...')
    # label image
    larr, num = label(arr < 2000, structure=np.ones((3,3,3)))
    # find COM of part
    partCOM = np.mean(np.argwhere(~larr), axis=0).astype(int)
    # find pore COM
    #poreCOM = csv[:,1:4].astype(int) + partCOM
    #csv[:,3] = csv[:,3].astype(int)
    poreCOM = csv[:,1:4] + partCOM
    # plot another pore
    fig = plt.figure()
    while True:
        prompt = 'Plot pore near what volume ({}, {})? '.format(csv[:,4].min(),
                                                                csv[:,4].max())
        try:
            lowVol = float(input(prompt))
        except:
            print("")
            break
        mask = csv[:,4] > lowVol
        dsub = csv[mask]
        psub = poreCOM[mask]
        idx = np.argmin(dsub[:,4])
        x,y,z = psub[idx]
        print("Pore volume {} um^3 at ({}, {}, {})".format(dsub[idx, 4], x, y, z))
        plt.cla()
        plt.imshow(arr[:,:,z], cmap='bone')
        plt.scatter([y],[x],s=10,c='r')
        #plt.scatter([x], [y], s=10, c='r')
        #plt.xticks([])
        #plt.yticks([])
        plt.show()

def main():
    # check command line
    if len(sys.argv) < 2:
        sys.stderr.write('Usage: {} multilayer.tif\n'.format(sys.argv[0]))
        sys.exit(1)
    # read .tif
    plot_com(sys.argv[1])

# plt.imshow(intensity_array[320,:,:], cmap='bone')
# plt.scatter(544.5, 1024-325, s=10, c='r')


if __name__ == '__main__':
    main()
