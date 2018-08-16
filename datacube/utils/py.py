import importlib
import logging
from contextlib import contextmanager

_LOG = logging.getLogger(__name__)


def import_function(func_ref):
    """
    Import a function available in the python path.

    Expects at least one '.' in the `func_ref`,
    eg:
        `module.function_name`
        `package.module.function_name`

    :param func_ref:
    :return: function
    """
    module_name, _, func_name = func_ref.rpartition('.')
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


@contextmanager
def ignore_exceptions_if(ignore_errors):
    """Ignore Exceptions raised within this block if ignore_errors is True"""
    if ignore_errors:
        try:
            yield
        except OSError as e:
            _LOG.warning('Ignoring Exception: %s', e)
    else:
        yield


class cached_property(object):  # pylint: disable=invalid-name
    """
    A property that is only computed once per instance and then replaces
    itself with an ordinary attribute. Deleting the attribute resets the
    property.

    Source: https://github.com/bottlepy/bottle/commit/fa7733e075da0d790d809aa3d2f53071897e6f76
    """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value