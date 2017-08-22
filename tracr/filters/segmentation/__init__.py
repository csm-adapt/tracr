from .otsu import tracr_otsu
from .threshold import register_threshold

# simple wrappers
from skimage.filters import (
    threshold_otsu as skimage_otsu,
    threshold_yen as skimage_yen,
    threshold_li as skimage_li,
    threshold_adaptive as skimage_adaptive
)
register_threshold(tracr_otsu)
register_threshold(skimage_otsu)
register_threshold(skimage_yen)
register_threshold(skimage_yi)
register_threshold(skimage_adaptive)
