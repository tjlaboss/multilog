"""
Processor

Module containing Processor class and helper functions
"""

import logging
import numpy as np
import multiprocessing as mp


def get_default_logger():
	return logging.getLogger(__name__)


class Processor:
	"""Multiprocessor with logging to a single file"""
	def __init__(self, n, placeholder=np.nan, logger=None):
		self._n = n
		self._placeholder = placeholder
		if logger is None:
			logger = get_default_logger()
		self._logger = logger

