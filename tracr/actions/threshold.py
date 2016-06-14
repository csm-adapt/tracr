from .base import Action
from subprocess import check_output


class Threshold(Action):
    """
    Base class for thresholding actions.
    """
    def __init__(self, *args, **kwds):
        super(Threshold, self).__init__(*args, **kwds)
        self.command = kwds.get('command', None)
        self.kwds = kwds.get('kwds', {})

    def __call__(self, *args, **kwds):
        if self.command is None:
            msg = 'No threshold command was provided.'
            raise ValueError(msg)
        kwds.update(self.kwds)
        self.command(*args, **kwds)
#end 'class Threshold(Action):'


class ExternalThreshold(Threshold):
    """
    Performs a thresholding operation.

    Example:

        ExternalThreshold(matlab, parameters=['imageThresholding.m'])

    Parameters
    --------
    :executable: the program to call

    Keywords
    --------
    :parameters: list of parameters to pass to the executable.
    """
    def __init__(self, executable, *args, **kwds):
        # handle optional parameters passed to the executable
        parameters = kwds.get('parameters', [])
        # fixed parameters
        # single value or string, otherwise already an iterable
        if not hasattr(parameters, '__iter__') or
            isinstance(parameters, str):
            parameters = [parameters]
        self.args = [[executable] + parameters]
        kwds['command'] = check_output
        # enable shell output
        # kwds['shell'] = True
        super(ExternalThreshold, self).__init__(self, *args, **kwds)

    def __call__(self, *args, **kwds):
        args = self.args + args
        super(ExternalThreshold, self).__call__(*args, **kwds)
#end 'class ExternalThreshold(Threshold):'
