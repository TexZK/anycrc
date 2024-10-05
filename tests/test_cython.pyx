# cython: language_level = 3
# cython: embedsignature = True
# cython: binding = True

# NOTES
# Assertion "is True/False" is to ensure the answer is EXACTLY the expected one.

import pytest as _

from anycrc.anycrc cimport *

# =====================================================================================================================

# Patch all Cython tests so that they can be discovered by pytest.
# Requires cython option: binding = True
def _patch_cytest():
    import functools
    import inspect

    def cytest(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            bound = inspect.signature(func).bind(*args, **kwargs)
            return func(*bound.args, **bound.kwargs)

        return wrapped

    g = globals()
    for key, value in g.items():
        if hasattr(value, '__name__'):
            if callable(value) and value.__name__.startswith('test_'):
                g[key] = cytest(value)


_patch_cytest()
