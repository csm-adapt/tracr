import .segmentation
from .segmentation import otsu

THRESHOLDS_ = {}

def register_threshold(func):
    THRESHOLDS_[func.__name__] = func

def threshold(*args, **kwds):
    """
    Thresholding divides an image into discrete regions based on intensity.
    These can be divided into ...

    """.append(
        "\n".join("""
        *{key:}*
        {doc:}""".format(key=k, doc=v.__doc__) for k,v in THRESHOLDS_.iteritems())
    )
    method = THRESHOLDS_.get(
        kwds.get('method', otsu),
        kwds.get('method', otsu))
    if 'method' in kwds:
        del kwds['method']
    return method(*args, **kwds)
