from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        lst = list(map(int, line.split()))
        for a, b in itertools.combinations(lst, r=2):
            if a % b == 0:
                total += a // b
            if b % a == 0 and b != a:
                total += b // a

    return total


INPUT_S = '''\
5 9 2 8
9 4 7 3
3 8 6 5
'''
EXPECTED = 9


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
