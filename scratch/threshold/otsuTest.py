import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math

from scipy import misc
from scipy import ndimage

# Read in a 3D array
im = misc.imread('C:\\Users\\andyp\\Documents\\RESEARCH\\xray\\tomo images\\C12-0.4X\\Multilayer Tiff\\C12-0.4X0096.tif')



def trilevel_otsu(image, bins=0):

	np.seterr(divide='ignore')

	im_max = np.amax(image)
	im_min = np.amin(image)
	N = image.shape[0]*image.shape[1]
	rows = image.shape[0]
	cols = image.shape[1]

	im_norm = (image.astype(float) - im_min)/(im_max-im_min)
	# Hitogram creation
	if(bins <= 0):
		bins = math.ceil(math.sqrt(2**16))



	#im_hist = np.zeros((1,bins))
	#for i in range(1,rows):
	#	for j in range(1,cols):
	#		tt = math.floor(bins*im_norm[i,j])
	#		if(tt==bins):
	#			tt=bins-1
	#		im_hist[0,tt] += 1

	im_hist,bin_edges = np.histogram(image,bins)
	bins = im_hist.size
	im_hist = im_hist.reshape((1,bins))

	im_prob = im_hist.astype("double")/N
	#print "Bins = " + str(bins)
	#print "Performing otsu"

	prob_table = (np.matmul(im_prob.transpose(),np.ones((1,bins)))).transpose()
	#i_table = np.matmul(np.expand_dims(np.arange(bins),axis=0).transpose(),np.ones((1,bins))).transpose()
	pi_table = prob_table*np.matmul(np.expand_dims(np.arange(bins),axis=0).transpose(),np.ones((1,bins))).transpose()

	P_table = np.zeros((bins,bins))
	S_table = np.zeros((bins,bins))

	for i in range(1,int(bins)):
		sumMask = np.triu(np.ones((bins,bins)))
		sumMask[:,i:bins-1] = 0

		P_table[:,i] = np.sum(sumMask*prob_table,1)
		S_table[:,i] = np.sum(sumMask*pi_table,1)

	H_table = np.divide(S_table**2,P_table)

	m=0;
	ind = np.zeros((1,2))

	for i in range(1,int(bins)-1):
		for j in range(i,int(bins)):
			tm = H_table[1-1,i-1] + H_table[i+1-1,j-1] + H_table[j-1,bins-1]
			if(tm > m):
				m=tm
				ind[0,0]=i
				ind[0,1]=j

	ind = (ind/bins)*(im_max-im_min) - im_min

	return (ind[0,0],ind[0,1])
	#print type(bins)
	#plt.plot(im_hist)
	#plt.imshow(H_table)
	#plt.show()


x = trilevel_otsu(im,0)
print x
