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
        try:
            self.command(*args, **kwds)
        except Exception, e:
            msg = 'Failed to execute ' \
                  '"{}({}, {})"'.format(self.command, args, kwds)
            raise type(e)(msg)
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
        # verify that the executable exists
        try:
            open(executable, 'r').close()
        except IOError:
            raise IOError('Cannot access {}.'.format(executable))
        # handle optional parameters passed to the executable
        parameters = kwds.get('parameters', [])
        # fixed parameters
        # single value or string, otherwise already an iterable
        if not hasattr(parameters, '__iter__') or \
            isinstance(parameters, str):
            parameters = [parameters]
        self.args = ([executable] + parameters,)
        kwds['command'] = check_output
        # enable shell output
        #kwds['shell'] = True
        super(ExternalThreshold, self).__init__(self, *args, **kwds)

    def __call__(self, *args, **kwds):
        try:
            # append user provided parameters to the list of
            # positional parameters
            args = self.args + args
            super(ExternalThreshold, self).__call__(*args, **kwds)
            # TODO: handle the return value of the external function
        except Exception, e:
            msg = ' '.join((
                'ExternalThreshold command:',
                str(self.command),
                str(*self.args)))
            raise type(e)(msg)
#end 'class ExternalThreshold(Threshold):'
