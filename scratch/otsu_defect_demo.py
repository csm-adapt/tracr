

#get_ipython().magic('matplotlib inline')
import sys, os
import glob
sys.path.append('..')
from tracr.actions.threshold import otsu
from PIL import Image
from skimage import filters
import numpy as np
from scipy.ndimage.measurements import center_of_mass, label
from matplotlib import pyplot as plt


# In[46]:

# Import sample datasets
A13_tifs = glob.glob('../test/test_resources/A13_0.4X_raw_tifs/*tif')
G04_tifs = glob.glob('../test/test_resources/A04_0.4X_raw_tifs/*tif')
M03_tifs = glob.glob('../test/test_resources/M03_0.4X_raw_tifs/*tif')
Y23_tifs = glob.glob('../test/test_resources/Y23_0.4X_raw_tifs/*tif')
imA13 = Image.open('../test/test_resources/A13_0.4X_raw_tifs/Layers_A13-0.4X0500.tif')
imG04 = Image.open('../test/test_resources/G04_0.4X_raw_tifs/G04-0.4X0500.tif')
imM03 = Image.open('../test/test_resources/M03_0.4X_raw_tifs/M03-0.4X0500.tif')
imY23 = Image.open('../test/test_resources/Y23_0.4X_raw_tifs/Y23-0.4X0500.tif')

A13_arr = np.zeros((imA13.size[::-1]+(len(A13_tifs),)))
G04_arr = np.zeros((imG04.size[::-1]+(len(G04_tifs),)))
M03_arr = np.zeros((imM03.size[::-1]+(len(M03_tifs),)))
Y23_arr = np.zeros((imY23.size[::-1]+(len(Y23_tifs),)))

for layer in range(len(A13_tifs)):
    A13_arr[:,:,layer] = np.array(Image.open(A13_tifs[layer]))
for layer in range(len(G04_tifs)):
    G04_arr[:,:,layer] = np.array(Image.open(G04_tifs[layer]))
for layer in range(len(M03_tifs)):
    M03_arr[:,:,layer] = np.array(Image.open(M03_tifs[layer]))
for layer in range(len(Y23_tifs)):
    Y23_arr[:,:,layer] = np.array(Image.open(Y23_tifs[layer]))


# In[42]:

# # TRACR thresholding
# A13_tracr_val = otsu(A13_arr)
# G04_tracr_val = otsu(G04_arr)
# M03_tracr_val = otsu(M03_arr)
# Y23_tracr_val = otsu(Y23_arr)
# A13_tracr = (A13_arr<A13_tracr_val)
# G04_tracr = (G04_arr<G04_tracr_val)
# M03_tracr = (M03_arr<M03_tracr_val)
# Y23_tracr = (Y23_arr<Y23_tracr_val)
# # SK Otsu thresholding
# A13_skotsu_val = filters.threshold_otsu(A13_arr)
# G04_skotsu_val = filters.threshold_otsu(G04_arr)
# M03_skotsu_val = filters.threshold_otsu(M03_arr)
# Y23_skotsu_val = filters.threshold_otsu(Y23_arr)
# A13_skotsu = (A13<A13_skotsu_val)
# G04_skotsu = (G04<G04_skotsu_val)
# M03_skotsu = (M03<M03_skotsu_val)
# Y23_skotsu = (Y23<Y23_skotsu_val)
# # SK Yen thresholding
# A13_skyen_val = filters.threshold_otsu(A13_arr)
# G04_skyen_val = filters.threshold_otsu(G04_arr)
# M03_skyen_val = filters.threshold_otsu(M03_arr)
# Y23_skyen_val = filters.threshold_otsu(Y23_arr)
# A13_skyen = (A13<A13_skyen_val)
# G04_skyen = (G04<G04_skyen_val)
# M03_skyen = (M03<M03_skyen_val)
# Y23_skyen = (Y23<Y23_skyen_val)



# In[ ]:

# Labeling and void data

part_list = [A13_arr, G04_arr, M03_arr, Y23_arr]
names = ["A13", "G04", "M03", "Y23"]
thresh_table = np.zeros((4,4))

for i in range(len(part_list)):
    part = part_list[i]
    name = names[i]

#     if i==0:
#         thresh_table[i,:] = part_list

    for j in range(3):

        if j==0:
            tracr_val = otsu(part)
            arr = (part<tracr_val)
            lbl, num = label(arr, np.ones((3,3,3)))
            thresh_table[j,i] = num
        if j==1:
            skotsu_val = filters.threshold_otsu(part)
            arr = (part<skotsu_val)
            lbl, num = label(arr, np.ones((3,3,3)))
            thresh_table[j,i] = num
        if j==2:
            skyen_val = filters.threshold_yen(part)
            arr = (part<skyen_val)
            lbl, num = label(arr, np.ones((3,3,3)))
            thresh_table[j,i] = num

        fig = plt.figure()
        ax11 = fig.add_subplot(221)
        ax12 = fig.add_subplot(222)
        ax21 = fig.add_subplot(223)
        ax22 = fig.add_subplot(224)
        ax11.imshow(part[:,:,500])
        ax12.imshow(part[:,:,500]<tracr_val)
        ax21.imshow(part[:,:,500]<skotsu_val)
        ax22.imshow(part[:,:,500]<skyen_val)
        plt.title(name)
        plt.show()

print thresh_table



# In[ ]:
