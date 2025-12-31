from __future__ import annotations

import argparse
import itertools
import os.path
from collections.abc import Iterator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def elevator(n: int) -> Iterator[int]:
    return itertools.cycle(list(range(n)) + list(range(n - 2, 0, -1)))


def compute(s: str) -> int:
    lines = s.splitlines()
    firewall = dict()
    max_depth = 0
    total = 0
    depths = {}

    for line in lines:
        layer, depth = list(map(int, line.split(': ')))
        firewall[layer] = elevator(depth)
        max_depth = max(max_depth, layer)
        depths[layer] = depth

    # initial setup:
    state = [-1] * (max_depth + 1)
    for k, v in firewall.items():
        state[k] = next(v)
    pos = 0

    for i in range(max_depth + 1):
        pos += 1
        if state[i] == 0:
            total += i * depths[i]
        for k, v in firewall.items():
            state[k] = next(v)
    return total


INPUT_S = '''\
0: 3
1: 2
4: 4
6: 4
'''
EXPECTED = 24


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
