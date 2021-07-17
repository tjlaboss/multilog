"""
Processor

Module containing Processor class and helper functions.
This StackOverflow thread was helpful: https://stackoverflow.com/q/10415028
"""

import logging
import numpy as np
import multiprocessing as mp


def get_default_logger():
	return logging.getLogger(__name__)


class Processor:
	"""Multiprocessor with logging to a single file
	
	Parameters:
	-----------
	n: int
		Number of processes
	
	placholder: object: optional
		What to return in place of a valid result
		[Default: np.nan]
	
	logger: logging.Logger; optional
		Existing logger to use.
		If not provided, one that I like will be created.
	"""
	def __init__(self, n, placeholder=np.nan, logger=None):
		assert isinstance(n, int) and n > 0, "n must be a positive integer."
		self._n = n
		self._placeholder = placeholder
		if logger is None:
			logger = get_default_logger()
		self._logger = logger
		
	def __len__(self):
		return self._n
	
	def __str__(self):
		ret = f"<{self.__class__.__name__}>"
		ret += f" ({self._n} processes, placeholder={self._placeholder})"
		return ret
	
	@property
	def n(self):
		return self._n
	
	@property
	def placeholder(self):
		return self._placeholder
	
	@property
	def logger(self):
		return self._logger

