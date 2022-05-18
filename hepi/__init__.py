"""The HEPi package aims to automize cluster computations for parameter scans with the option to produce plots."""
from .output import *
from .input import *
from .results import *
from .util import *
from .plot import *
from .run import *
from .load import *

import pkg_resources as pkg  # part of setuptools
#import json
#import requests
#from urllib.request import urlopen

package = "hepi"

try:
    version = pkg.require(package)[0].version
except pkg.DistributionNotFound:
    version = "dirty"

__version__ = version