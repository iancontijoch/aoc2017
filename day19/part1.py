from __future__ import annotations

import argparse
import os.path
from collections import deque
from string import ascii_uppercase
from typing import Deque

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> str:
    lines = s.splitlines()

    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }
    letters = []

    def cand_dirs(
        pos: tuple[int, int], d: Direction4,
    ) -> list[Direction4]:
        if coords[pos] in ('|', '-'):
            return [d]
        elif coords[pos] in ascii_uppercase:
            letters.append(coords[pos])
            return [d]
        elif coords[pos] == '+':
            return [dir for dir in Direction4 if dir != d.opposite]
        else:
            raise NotImplementedError

    start = (lines[0].find('|'), 0)
    q: Deque[tuple[tuple[int, int], Direction4]] = deque(
        [(start, Direction4.DOWN)],
    )
    seen = set()
    while q:
        pos, d = q.popleft()
        if (pos, d) in seen:
            continue
        seen.add((pos, d))
        for cand_dir in cand_dirs(pos, d):
            cand = cand_dir.apply(*pos)
            if cand in coords and coords[cand] != ' ' and cand not in seen:
                q.append((cand, cand_dir))

    return ''.join(letters)


INPUT_S = '''\
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
'''
EXPECTED = 'ABCDEF'


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
