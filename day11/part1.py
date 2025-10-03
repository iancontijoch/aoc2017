from __future__ import annotations

import argparse
import os.path
from collections import Counter

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def update(
    counter: Counter[str],
    dir1: str, dir2: str, dir3: str | None,
) -> Counter[str]:
    if dir1 in counter and dir2 in counter:
        if counter[dir1] >= counter[dir2]:
            counter[dir1] -= counter[dir2]
            if dir3 is not None:
                counter[dir3] += counter[dir2]
            counter[dir2] = 0
        else:
            counter[dir2] -= counter[dir1]
            if dir3 is not None:
                counter[dir3] += counter[dir1]
            counter[dir1] = 0
    return counter


def reduce(counter: Counter[str]) -> Counter[str]:
    dirs = (
        ('ne', 'nw', 'n'),
        ('se', 'sw', 's'),
        ('n', 's', None),
        ('se', 'nw', None),
        ('ne', 'sw', None),
        ('nw', 's', 'sw'),
        ('ne', 's', 'se'),
        ('se', 'n', 'ne'),
        ('sw', 'n', 'nw'),
    )

    for dir1, dir2, dir3 in dirs:
        counter = update(counter, dir1, dir2, dir3)
    return counter


def compute(s: str) -> int:
    line = s.splitlines()[0]
    moves = line.split(',')
    counter = Counter(moves)
    for _ in range(1000):
        counter = reduce(counter)
        pass
    return sum(counter.values())


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ne,ne,ne', 3),
        ('ne,ne,sw,sw', 0),
        ('ne,ne,s,s', 2),
        ('se,sw,se,sw,sw', 3),
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
