from __future__ import annotations

import argparse
import os.path
from functools import lru_cache

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OFFSET = 394


@lru_cache(maxsize=None)
def get_insert(
    pos: int,
    size: int,
    offset: int = OFFSET,
) -> int:
    return (pos + offset) % size


def compute(s: str) -> int:
    pos = 0
    k = 1
    size = 1
    digit = -1
    for _ in range(50_000_000):
        insert_pos = get_insert(pos, size)
        if insert_pos == 0:
            digit = k
        pos = insert_pos + 1
        k += 1
        size += 1
    return digit


INPUT_S = '''\

'''
EXPECTED = 638


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
