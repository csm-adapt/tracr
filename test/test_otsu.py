import sys
sys.path.append('..')
from tracr.actions.threshold import otsu
from PIL import Image
from scipy.misc import face
from skimage import feature, filters
import numpy as np
from matplotlib import pyplot as plt
from glob import glob

# ----- set up logging -----
import logging
logger = logging.getLogger('test-otsu')
ch = logging.StreamHandler() # create console handler
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s') # create a formatter
ch.setFormatter(formatter)
logger.addHandler(ch) # add console handler to logger
# ----- end set up logging -----

# To test, simply run
# [...]$ nosetests (optionally with -v)
# and a report a summary of the results

def array2image(arr):
    arr = np.asarray(arr).astype(np.uint8)
    rows, cols = arr.shape
    im = Image.new('L', (cols, rows))
    im.frombytes(arr.tobytes())
    return im



class TestClass: # keep this the same
    def setUp(self):
        # construct objects and perform any necessary setup
        # image = ImageSequence.Iterator('A05-0.4X.tif')
        # self.image = np.array([np.array(frame) for frame in image])
        # self.image = np.transpose(self.image, (1,2,0))
        self.image = face(gray=True)
        #array2image(self.image).show()

    def test_two_class_otsu(self):
        # run test one
        self.thresholds = otsu(self.image)
        logger.info("two-class: {}".format(self.thresholds))
        array2image(255*(self.image > self.thresholds[0])).show()
        assert np.isclose(self.thresholds[0], 115.72265625), \
            'Two-class Otsu threshold ({}) != {}'.format(
                self.thresholds[0], 115.72265625)

    def test_three_class_otsu(self):
        self.thresholds = otsu(self.image, nclasses=3)
        logger.info("three-classes: {}".format(self.thresholds))
        array2image(128*(self.image > self.thresholds[0]) +
                    127*(self.image > self.thresholds[1])).show()
        assert np.allclose(self.thresholds, (82.51953125, 145.01953125)), \
            'Three-class Otsu threshold [{}] != {}'.format(
                self.thresholds, (82.51953125, 145.01953125))

    def test_four_class_otsu(self):
        self.thresholds = otsu(self.image, nclasses=4)
        logger.info("four-classes: {}".format(self.thresholds))
        array2image( 85*(self.image > self.thresholds[0]) +
                    170*(self.image > self.thresholds[1]) +
                    255*(self.image > self.thresholds[2])).show()
        assert np.allclose(self.thresholds, (68.84765625, 123.53515625, 168.45703125)), \
            'Four-class Otsu threshold [{}] != {}'.format(
                self.thresholds, (68.84765625, 123.53515625, 168.45703125))

    def test_tif_series_2otsu_Y23(self):
        frame_list = glob("./test_resources/Y23_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            self.thresholds = otsu(self.image, nclasses=2)
            if idx==425:
                # Plot intensity histogram and thresholds
                plt.hist(self.image.flatten(), bins=256, log=True)
                for t in self.thresholds:
                    plt.axvline(t, color='r')
                plt.title('Y23 using class=2')
                plt.draw()
                plt.savefig('Y23_2-class.png', dpi=300)
                plt.clf()
                Image.open('Y23_2-class.png').show()

                # Plot actual data and thresholded
                edge = feature.canny(self.image>self.thresholds[0])
                highlight = np.copy(self.image)
                highlight[edge] = 2*self.image.max() - self.image.min()
                fig = plt.figure()
                ax11 = fig.add_subplot(221)
                ax12 = fig.add_subplot(222)
                ax21 = fig.add_subplot(223)
                ax22 = fig.add_subplot(224)
                ax11.imshow(self.image)
                ax12.imshow(self.image>self.thresholds[0])
                ax21.imshow(highlight)
                ax22.imshow(edge)
                plt.show()

    def test_tif_series_3otsu_Y23(self):
        frame_list = glob("./test_resources/Y23_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            self.thresholds = otsu(self.image, nclasses=3)
            if idx==425:
                plt.hist(self.image.flatten(), bins=256, log=True)
                for t in self.thresholds:
                    plt.axvline(t, color='r')
                plt.title('Y23 using class=3')
                plt.draw()
                plt.savefig('Y23_3-class.png')
                plt.clf()
                Image.open('Y23_3-class.png')

    def test_tif_series_2otsu_A13(self):
        frame_list = glob("./test_resources/A13_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            self.thresholds = otsu(self.image, nclasses=2)
            if idx==425:
                plt.hist(self.image.flatten(), bins=256, log=True)
                for t in self.thresholds:
                    plt.axvline(t, color='r')
                plt.title('A13 using class=2')
                plt.draw()
                plt.savefig('A13_2-class.png', dpi=300)
                plt.clf()
                Image.open('A13_2-class.png').show()

                # Plot actual data and thresholded
                edge = feature.canny(self.image>self.thresholds[0])
                highlight = np.copy(self.image)
                highlight[edge] = 2*self.image.max() - self.image.min()
                fig = plt.figure()
                ax11 = fig.add_subplot(221)
                ax12 = fig.add_subplot(222)
                ax21 = fig.add_subplot(223)
                ax22 = fig.add_subplot(224)
                ax11.imshow(self.image)
                ax12.imshow(self.image>self.thresholds[0])
                ax21.imshow(highlight)
                ax22.imshow(edge)
                plt.show()

    def test_tif_series_3otsu_A13(self):
        frame_list = glob("./test_resources/A13_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            self.thresholds = otsu(self.image, nclasses=3)
            if idx==425:
                plt.hist(self.image.flatten(), bins=256, log=True)
                for t in self.thresholds:
                    plt.axvline(t, color='r')
                plt.title('A13 using class=3')
                plt.draw()
                plt.savefig('A13_3-class.png', dpi=300)
                plt.clf()
                Image.open('A13_3-class.png').show()

    def test_tif_series_2otsu_M04(self):
        frame_list = glob("./test_resources/M04_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            self.thresholds = otsu(self.image, nclasses=2)
            if idx==425:
                plt.hist(self.image.flatten(), bins=256, log=True)
                for t in self.thresholds:
                    plt.axvline(t, color='r')
                plt.title('M04 using class=2')
                plt.draw()
                plt.savefig('M04_2-class.png', dpi=300)
                plt.clf()
                Image.open('M04_2-class.png').show()

                # Plot actual data and thresholded
                edge = feature.canny(self.image>self.thresholds[0])
                highlight = np.copy(self.image)
                highlight[edge] = 2*self.image.max() - self.image.min()
                fig = plt.figure()
                ax11 = fig.add_subplot(221)
                ax12 = fig.add_subplot(222)
                ax21 = fig.add_subplot(223)
                ax22 = fig.add_subplot(224)
                ax11.imshow(self.image)
                ax12.imshow(self.image>self.thresholds[0])
                ax21.imshow(highlight)
                ax22.imshow(edge)
                plt.show()

    def test_tif_series_3otsu_M04(self):
        frame_list = glob("./test_resources/M04_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            self.thresholds = otsu(self.image, nclasses=3)
            if idx==425:
                plt.hist(self.image.flatten(), bins=256, log=True)
                for t in self.thresholds:
                    plt.axvline(t, color='r')
                plt.title('M04 using class=3')
                plt.draw()
                plt.savefig('M04_3-class.png', dpi=300)
                plt.clf()
                Image.open('M04_3-class.png').show()

    def test_compare_thresholds(self):
        frame_list = glob("./test_resources/Y23_0.4X_raw_tifs/*.tif")
        for idx in range(400,450):
            frame = frame_list[idx]
            self.image = np.array(Image.open(frame))
            if idx==425:
                # Yen threshold seems to return same as TRACR
                self.otsu_thresholds = otsu(self.image, nclasses=2)
                self.sk_otsu = filters.threshold_otsu(self.image, nbins=256)
                self.sk_adaptive5 = filters.threshold_adaptive(self.image,
                                                               block_size=5)
                self.sk_adaptive21 = filters.threshold_adaptive(self.image,
                                                               block_size=21)
                self.sk_yen = filters.threshold_yen(self.image, nbins=256)
                plt.hist(self.image.flatten(), bins=256, log=True)

                # The adaptive implementations return thresholded arrays
                print "TRACR Otsu thresholds: %s" % (self.otsu_thresholds)
                print "SK Otsu thresholds: %s" % (self.sk_otsu)
                print "SK Yen thresholds: %s" % (self.otsu_thresholds)

                fig = plt.figure()
                ax11 = fig.add_subplot(231)
                ax12 = fig.add_subplot(232)
                ax13 = fig.add_subplot(233)
                ax21 = fig.add_subplot(234)
                ax22 = fig.add_subplot(235)
                ax23 = fig.add_subplot(236)
                ax11.imshow(self.image)
                ax12.imshow(self.image<otsu_thresholds[0])
                ax13.imshow(self.image<sk_otsu)
                ax21.imshow(sk_adaptive5)
                ax22.imshow(sk_adaptive21)
                ax23.imshow(self.image<sk_yen)
                plt.show()

    # def test_tif_series_4otsu(self):
    #     frame_list = glob("./test_resources/M04_0.4X_raw_tifs/*.tif")
    #     for idx in range(len(frame_list)):
    #         frame = frame_list[idx]
    #         self.image = np.array(Image.open(frame))
    #         self.thresholds = otsu(self.image, nclasses=4)
    #         if idx==500:
    #             plt.hist(self.image.flatten(), bins=256)
    #             for t in self.thresholds:
    #                 plt.axvline(t, color='r')
    #             plt.show()

    def tearDown(self):
        # clean up
        pass
        # plt.hist(self.image.flatten(), bins=256)
        # for t in self.thresholds:
        #     plt.axvline(t, color='r')
        # plt.show()
