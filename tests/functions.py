# Simple functions to test
import time
from assets import REDUCTION


def f1(t, logger):
	value = t**2
	t /= REDUCTION
	logger.info(f"Working for {t:.3f} seconds.")
	time.sleep(t)
	return value


def f2(t1, t2, logger):
	value = t1 + t2
	t1 /= REDUCTION
	t2 /= REDUCTION
	logger.info(f"Working for {t1:.3f} + {t2:.3f} seconds.")
	time.sleep(t1 + t2)
	return value


def dummy_f(tag, logger):
	logger.debug(f"Launching dummy_f(tag={repr(tag)})")
	if not tag:
		logger.warning("Tag not found.")
		ret = 1
	else:
		logger.info(f">>> {tag} <<<")
		ret = 0
	logger.info("Done.")
	return ret
