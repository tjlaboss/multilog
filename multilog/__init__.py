__version_info__ = (0, 0, 1)
__version__ = ".".join([str(x) for x in __version_info__])
__author__ = "Travis J. Labossiere-Hickman (@tjlaboss)"

from . import processor
from .processor import Processor
