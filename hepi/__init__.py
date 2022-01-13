from .input import *
from .results import *
from .util import LD2DL
from .plot import *

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