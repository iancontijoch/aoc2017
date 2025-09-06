from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)
    i = j = counter = 0
    off = 0
    while i < len(numbers):
        if counter != 0:
            numbers[j] += 1 if off < 3 else -1
        j = i
        off = numbers[i]
        i += off
        counter += 1
    return counter


INPUT_S = '''\
0
3
0
1
-3
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
