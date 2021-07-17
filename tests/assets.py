# Some testing materials

LIST_TIMES = (1, 2, 4, 8)
N = len(LIST_TIMES)
TUPLE1_TIMES = [(_,) for _ in LIST_TIMES]
TUPLE2_TIMES = [(_, _+1) for _ in LIST_TIMES]
DICT1_TIMES = [{"t": _} for _ in LIST_TIMES]
DICT2_TIMES = [{"t1": _, "t2": _+1} for _ in LIST_TIMES]
F1_RESULTS = [1, 4, 16, 64]
F2_RESULTS = [3, 5, 9, 17]
REDUCTION = 100
