from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    numbers = support.parse_numbers_split(s)

    def pt_1(numbers: list[int]) -> tuple[int, list[int]]:
        count = 0
        size = len(numbers)
        seen = {tuple(numbers)}
        while True:
            max_i, max_amt = max(
                enumerate(numbers),
                key=lambda x: (x[1], -x[0]),
            )
            left = max_amt
            numbers[max_i] = 0
            i = max_i
            while left > 0:
                i = (i + 1) % size
                numbers[i] += 1
                left -= 1
            count += 1
            if tuple(numbers) in seen:
                return (count, numbers)
            tup_numbers = tuple(numbers)
            seen.add(tup_numbers)

    _, repeat = pt_1(numbers)
    i2, _ = pt_1(repeat)
    return i2


INPUT_S = '''\
0 2 7 0
'''
EXPECTED = 4


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
