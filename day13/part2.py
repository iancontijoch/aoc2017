from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def cycle(n: int, t: int) -> int:
    return (n - 1) - abs((n - 1) - (t % (2 * n - 2)))


def compute(s: str) -> int:
    lines = s.splitlines()
    max_depth = 0
    depths = {}

    for line in lines:
        layer, depth = list(map(int, line.split(': ')))
        max_depth = max(max_depth, layer)
        depths[layer] = depth

    depths_lst = [-1] * (max_depth + 1)
    for k, v in depths.items():
        depths_lst[k] = v

    delay = 0
    while True:
        if 0 not in [cycle(d, delay + i) for i, d in enumerate(depths_lst)]:
            break
        else:
            delay += 1
    return delay


INPUT_S = '''\
0: 3
1: 2
4: 4
6: 4
'''
EXPECTED = 10


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
