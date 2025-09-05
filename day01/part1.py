from __future__ import annotations

import argparse
import os.path

import pytest
import itertools

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    line = s.splitlines()[0]

    return sum(
        int(n_s) 
        for i, n_s in enumerate(line)
        if int(n_s) == int(line[(i + 1) % len(line)])
    )        

INPUT_S = '''\

'''
EXPECTED = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1122', 3),
        ('1111', 4),
        ('1234', 0),
        ('91212129', 9)
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
