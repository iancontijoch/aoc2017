from __future__ import annotations

import argparse
import math
import os.path
from collections import deque
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
Coords: TypeAlias = dict[tuple[int, int], int]


def solve(
    start: tuple[int, int],
    width: int,
    limit_s: str,
) -> int:
    coords = {(x, y): 0
              for x in range(width + 1)
              for y in range(width + 1)}
    coords[start] = 1

    def bfs(
        start: tuple[int, int],
        end: str,
        seen: set[tuple[int, int]] | None = None,
    ) -> int:
        if seen is None:
            seen = set()
        q = deque([(start, 1, support.Direction4.DOWN)])
        while q:
            pos, n, dir = q.popleft()
            if pos in seen:
                continue

            if pos not in coords:
                continue

            val = sum(
                coords[adj]
                for adj in support.adjacent_8(*pos) if adj in coords
            )

            if val > int(limit_s):
                return val

            if pos != start:
                coords[pos] = val

            if coords[pos] == end:
                seen.add(pos)
                break

            seen.add(pos)
            left_turn = (dir.ccw.apply(*pos), (n + 1), dir.ccw)
            str8_turn = (dir.apply(*pos), (n + 1), dir)

            q.appendleft(str8_turn)
            q.appendleft(left_turn)

        return -1

    return bfs(start, limit_s)


def compute(s: str) -> int:
    lines = s.splitlines()
    num_s = lines[0]
    width = math.ceil(math.sqrt(int(num_s)))
    start = (width // 2, width // 2)

    total = solve(start=start, width=width, limit_s=num_s)
    return total


INPUT_S = """\

"""
EXPECTED = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1', 0),
        ('12', 3),
        ('23', 2),
        ('1024', 31),
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
