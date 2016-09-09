from tracr.actions.trilevel_otsu import trilevel_otsu

class TestClass:
    def setUp(self):
        self.im = np.load('A13_raw.npy')

    def test_trilevel_otsu(self):
        # perform a threshold on an image you've already characterized,
        # let's say those levels are L and U (for lower and upper thresholds, respectively)
        thresholds = trilevel_otsu(self.im[500], bins=0)
        assert np.allcose(thresholds, (L, U)), \
            'Thresholds do not match expected levels: {} != {}'.format(thresholds, (L, U))
