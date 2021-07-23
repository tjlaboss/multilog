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


if __name__ == '__main__':
	dummy_logger = _get_logger()
	dummy_logger.info("Testing dummy logger.")
