"""The HEPi package aims to automize cluster computations for parameter scans with the option to produce plots."""
from importlib.metadata import version

from .input import *
from .interpolate import *
from .load import *
from .output import *

# TODO remvoe this for speed
from .plot import *
from .results import *
from .run import *
from .util import *

# import pkg_resources as pkg  # part of setuptools
# import json
# import requests
# from urllib.request import urlopen
from ._version import version as __version__

package = "hepi"
__all__ = ["__version__"]


# try:
#    version = pkg.require(package)[0].version
# except pkg.DistributionNotFound:
#    version = "dirty"
# __version__ = version
#
