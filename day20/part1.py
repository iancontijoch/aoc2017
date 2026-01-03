from __future__ import annotations

import argparse
import os.path
import re

import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
TOTAL_T = 1000


def manhattan(arr: np.ndarray) -> int:
    return np.sum(np.abs(arr))


def compute(s: str) -> int:
    lines = s.splitlines()
    dists = []
    for line in lines:
        p, v, a = (
            list(map(int, m.split(',')))
            for m in re.findall(r'(-*\d+,-*\d+,-*\d+)', line)
        )
        P, V, A = np.array(p), np.array(v), np.array(a)
        for t in range(1, TOTAL_T):
            P += V + t * A
        dists.append(manhattan(P))
    return int(np.argmin(dists))


INPUT_S = '''\
p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>
'''
EXPECTED = 0


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
