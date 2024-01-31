__version__ = '1.0'

from .format import *
from .stats import *
from .generator import *



# add to top level __init__.py so we can use like this:
# import geofreak as gfk
# gfk.from_numpy_to_tiff(...)