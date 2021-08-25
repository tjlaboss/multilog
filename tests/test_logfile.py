# Test reading the contents of the log file.

import logging
from functions import dummy_f
import sys; sys.path.append('..')
import multilog

FULL_FMT = "%(name)s: %(filename)s:%(lineno)s - %(levelname)s: %(message)s"
FULL_FILE = "full.log"
TEST_FMT = "%(name)s - %(levelname)s: %(message)s"
TEST_FILE = "test.log"


def _get_logger():
	test_logger = logging.getLogger("test")
	test_logger.setLevel(1)
	# Full logging to file handler 1. For debugging purposes.
	fh1 = logging.FileHandler(FULL_FILE, mode='w')
	fh1.setFormatter(logging.Formatter(FULL_FMT))
	fh1.setLevel(logging.DEBUG)
	test_logger.addHandler(fh1)
	# Reduced logging to file handler 2. For generating test results.
	fh2 = logging.FileHandler(TEST_FILE, mode='w')
	fh2.setFormatter(logging.Formatter(TEST_FMT))
	fh2.setLevel(logging.INFO)
	test_logger.addHandler(fh2)
	return test_logger


def _check_file(log_file, ref_file):
	"""Check the contents of a log file, order not important."""
	with open(log_file, 'r') as f1:
		log_lines = f1.readlines()
		log_lines.sort()
	with open(ref_file, 'r') as f2:
		ref_lines = f2.readlines()
		ref_lines.sort()
	errstr = "Log file {} does not match reference file {}!"
	assert log_lines == ref_lines, errstr.format(repr(log_file), repr(ref_file))


def test_dummy():
	dummy_logger = _get_logger()
	dummy_logger.info("Testing dummy logger.")
	mlp = multilog.Processor(3, logger=dummy_logger)
	mlp.run(dummy_f, arglist=[(2,), ('one',), (None,)])
	results = mlp.wait()
	results.sort()
	dummy_logger.info("Got results: {}".format(results))
	_check_file(TEST_FILE, "dummy.ref")
	print("test_dummy() passed.")


if __name__ == '__main__':
	test_dummy()
