# PYTHON INTERPRETATION OF ANDY'S MATLAB RDF SCRIPT. GENERATES AN RDF
# FOR A SAMPLE SET OF 2D DATA -HG

from __future__ import division
import numpy as np
from matplotlib import pyplot as plt

## Generate datapoints --------------------
N = 100

# random distribution
points = np.random.rand(N,2)*30 - 15

# square lattice
# points = np.zeros((N,2))
# for i in range(10):
#     for j in range(10):
#         points[10*i+j,0] = i
#         points[10*i+j,1] = j

## Geometry --------------------
dr = 0.1

# domain bounds
x_bound = np.array([np.min(points[:,0]), np.max(points[:,0])])
y_bound = np.array([np.min(points[:,1]), np.max(points[:,1])])

width = x_bound[1] - x_bound[0]
height = y_bound[1] - y_bound[0]

rho_overall = N/(width*height)
rmax = np.min(np.array([width, height]))/2
numAnnuli = np.ceil(rmax/dr).astype(int)

## Computing --------------------
rdf = np.zeros((1,numAnnuli))

# loop through each point as a reference
for i in range(N):

    distances = np.zeros(N)
    # check distance of each neighbor
    for j in range(N):
        if i!=j:
            d = np.sqrt((points[j,0]-points[i,0])**2+(points[j,1]-points[i,1])**2)
            distances[j] = d
    [hist, bin_edges] = np.histogram(distances, numAnnuli)
    rdf = rdf + hist/(2*np.pi*bin_edges*dr*rho_overall)

plt.scatter(bin_edges, rdf)
plt.imshow()
