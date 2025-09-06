from __future__ import annotations

import argparse
import os.path
from collections import Counter
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    totals = 0
    for line in lines:
        seen: set[Any] = set()
        flag = True
        for word in line.split():
            counter = tuple(sorted(Counter(word).items()))
            if counter in seen:
                flag = False
                break
            seen.add(counter)
        totals += bool(flag)
    return totals


INPUT_S = '''\

'''
EXPECTED = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # ('abcde fghij', 1),
        ('abcde xyz ecdab', 0),
        ('a ab abc abd abf abj', 1),
        ('iiii oiii ooii oooi oooo', 1),
        ('oiii ioii iioi iiio', 0),
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
