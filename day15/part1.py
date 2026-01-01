from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
N_PAIRS = 40_000_000


def compute(s: str, n_pairs: int) -> int:
    lines = s.splitlines()
    total = 0
    a = int(lines[0].split()[-1])
    b = int(lines[1].split()[-1])

    def next_value(prev: int, gen: str) -> int:
        FACTOR = 16807 if gen == 'a' else 48271
        prev *= FACTOR
        return prev % 2147483647

    def check(a: int, b: int) -> bool:
        return bin(a)[-16:] == bin(b)[-16:]

    for _ in range(n_pairs):
        a = next_value(a, 'a')
        b = next_value(b, 'b')
        if check(a, b):
            total += 1
    return total


INPUT_S = '''\
Generator A starts with 65
Generator B starts with 8921
'''
EXPECTED = 588


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 40_000_000) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 40_000_000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
