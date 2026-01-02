from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OFFSET = 394


def get_insert(
    pos: int,
    size: int,
    offset: int = OFFSET,
) -> int:
    return (pos + offset) % size


def compute(s: str) -> int:
    pos = 0
    k = 1
    buffer = [0]
    for _ in range(2017):
        insert_pos = get_insert(pos, len(buffer)) + 1
        buffer.insert(insert_pos, k)
        pos = insert_pos
        k += 1
    return buffer[pos+1]


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
