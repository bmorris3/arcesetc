# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Licensed under a 3-clause BSD style license - see LICENSE.rst
try:
    from .version import version as __version__
except ImportError:
    __version__ = ''


from .plots import *
from .util import *
