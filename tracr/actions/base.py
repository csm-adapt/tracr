class Action(object):
    """
    Base class for handling actions that are to be performed by tracr.
    """
    def __init__(self, *args, **kwds):
        pass

    def __call__(self, *args, **kwds):
        msg = 'Development Error: Classes that derive from Action must ' \
              'implement __call__.'
        raise NotImplementedError(msg)
#end 'class Action(object):'
