# Test arg and kwarg passing

from assets import *
from functions import f1, f2
import sys; sys.path.append('..')
import multilog


def test_1arg():
	p_1arg = multilog.Processor(N)
	p_1arg.run(f1, TUPLE1_TIMES)
	results = p_1arg.wait()
	results.sort()
	assert results == F1_RESULTS, f"test_1arg() failed: {results}"
	print("test_1arg() passed")
	return 0


def test_1kwarg():
	p_1kwarg = multilog.Processor(N)
	p_1kwarg.run(f1, kwarglist=DICT1_TIMES)
	results = p_1kwarg.wait()
	results.sort()
	assert results == F1_RESULTS, f"test_1kwarg() failed: {results}"
	print("test_1kwarg() passed")
	return 0


def test_2args():
	p_2args = multilog.Processor(N)
	p_2args.run(f2, TUPLE2_TIMES)
	results = p_2args.wait()
	results.sort()
	assert results == F2_RESULTS, f"test_2args() failed: {results}"
	print("test_2args() passed")
	return 0


def test_2kwargs():
	p_2kwargs = multilog.Processor(N)
	p_2kwargs.run(f2, kwarglist=DICT2_TIMES)
	results = p_2kwargs.wait()
	results.sort()
	assert results == F2_RESULTS, f"test_2kwargs() failed: {results}"
	print("test_2kwargs() passed")
	return 0


def test_1arg_1kwarg():
	p_1arg_1kwarg = multilog.Processor(N)
	p_1arg_1kwarg.run(f2, arglist=TUPLE1_TIMES, kwarglist=[{"t2": d["t2"]} for d in DICT2_TIMES])
	results = p_1arg_1kwarg.wait()
	results.sort()
	assert results == F2_RESULTS, f"test_2kwargs() failed: {results}"
	print("test_1arg_1kwarg() passed")
	return 0


def main():
	print("You are not running using PyTest.")
	test_1arg()
	test_1kwarg()
	test_2args()
	test_2kwargs()
	test_1arg_1kwarg()
	print("All tests passed.")


if __name__ == "__main__":
	main()
