"""
Processor

Module containing Processor class and helper functions.
This StackOverflow thread was helpful: https://stackoverflow.com/q/10415028
"""

import atexit
import logging
import numpy as np
import multiprocessing as mp


def get_default_logger():
	return logging.getLogger(__name__)


def get_process_logger(i: int, n: int, base_logger: logging.Logger):
	"""Get a numbered process logger in the appropriate namespace
	
	Get a named process logger.
	The process logger will use the list of handlers of base_logger.
	If base_logger has a name, the process logger will be in that namespace.
	
	Examples:
	---------
	>>> get_process_logger(1, 1, logging.Logger("foo"))
	< Logger foo.1 >
	>>> get_process_logger(1, 10, logging.Logger("bar"))
	< Logger bar.01 >
	>>> get_process_logger(10, 10, logging.Logger())
	< Logger 10 >
	
	Parameters:
	-----------
	i: int
		ID of this logger
	
	n: int
		Total number of process loggers.
		Only used for padding name with zeros.
		
	base_logger: logging.Logger
		Existing logger to base the namespace and handlers on.
	
	Returns:
	--------
	process_logger: logging.Logger
		New (or existing) logger, with handlers set to base_logger.handlers.
	"""
	if n == 1:
		iname = "1"
	else:
		nd = np.ceil(np.log10(n+1))
		iname = f"{{:0{nd:.0f}d}}".format(i)
	if base_logger.name:
		iname = f"{base_logger.name}.{iname}"
	process_logger = logging.getLogger(iname)
	process_logger.handlers = base_logger.handlers
	return process_logger


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
		self._procs = [None]*n
		self._queue = mp.Queue(n)
		self._logger.debug(f"{self} instantiated.")
		atexit.register(self.kill)
		
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
	
	def _wrapper(self, f, f_args, f_kwargs, ilogger):
		"""Wrapper for whatever user function
		
		Parameters:
		-----------
		f: callable
			Function or other callable.
		
		f_args: tuple
			args to f(*args)
		
		f_kwargs: dict
			kwargs to f(**kwargs)
		
		ilogger: logging.Logger
			Appropriate process logger
		"""
		try:
			value = f(*f_args, **f_kwargs, logger=ilogger)
		except Exception as e:
			func_name = getattr(f, "__name__", repr(f))
			ilogger.exception(e)
			ilogger.error(f"Call to function {func_name} failed: {e}")
			value = self._placeholder
		self._queue.put(value)
	
	def _start_process(self, i, function, args, kwargs):
		ilogger = get_process_logger(i, self._n, self._logger)
		proc = mp.Process(target=self._wrapper, args=(function, args, kwargs, ilogger))
		proc.start()
		self._procs[i] = proc
	
	def run(self, function, args=None, kwargs=None):
		"""Start running multiprocessing a provided function with nice logging

		Parameters:
		-----------
		f: callable
			Function or other callable.
			Must accept 'logger=...' as an argument.
			May accept *args, **kwargs.

		f_args: tuple; optional
			args to function(*args)

		f_kwargs: dict; optional
			kwargs to f(**kwargs)
		"""
		for i, proc in enumerate(self._procs):
			if proc is None:
				self._start_process(i, function, args, kwargs)
			else:
				self._logger.warning(f"Process {i+1}/{self._n} is already running; skipping.")
	
	def kill(self):
		"""Kill all child processes"""
		for proc in self._procs:
			if proc is not None:
				proc.kill()
			self._procs = [None]*self._n

