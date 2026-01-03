from __future__ import annotations

import argparse
import os.path
import re
from collections import Counter

import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
TOTAL_T = 1000


def compute(s: str) -> int:
    lines = s.splitlines()
    Ps, Vs, As = [], [], []
    for line in lines:
        p, v, a = (
            list(map(int, m.split(',')))
            for m in re.findall(r'(-*\d+,-*\d+,-*\d+)', line)
        )
        p_arr, v_arr, a_arr = np.array(p), np.array(v), np.array(a)
        Ps.append(p_arr)
        Vs.append(v_arr)
        As.append(a_arr)

    P, V, A = np.vstack(Ps), np.vstack(Vs), np.vstack(As)
    for t in range(1, TOTAL_T):
        P += V + t * A
        duplicate_rows = [
            c for c, n in
            Counter(tuple(p.tolist()) for p in P).items()
            if n > 1
        ]

        to_delete = []
        for i, row in enumerate(P):
            if tuple(row.tolist()) in duplicate_rows:
                to_delete.append(i)

        P = np.delete(P, (to_delete), axis=0)
        V = np.delete(V, (to_delete), axis=0)
        A = np.delete(A, (to_delete), axis=0)

    return len(P)


INPUT_S = '''\
p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>
'''
EXPECTED = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
