from __future__ import annotations

import argparse
import math
import os.path
from collections import deque
from typing import TypeAlias

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
Coords: TypeAlias = dict[tuple[int, int], str]


def make_spiral(
    start: tuple[int, int],
    width: int,
    limit: str,
) -> Coords | None:
    coords = {(x, y): '0'
              for x in range(width + 1)
              for y in range(width + 1)}
    coords[start] = '(1)'

    def bfs(
        start: tuple[int, int],
        end: str,
        seen: set[tuple[int, int]] | None = None,
    ) -> Coords:
        if seen is None:
            seen = set()
        q = deque([(start, 1, support.Direction4.DOWN)])
        while q:
            pos, n, dir = q.popleft()
            if pos in seen:
                continue

            if pos not in coords:
                continue

            coords[pos] = str(n)
            if coords[pos] == end:
                seen.add(pos)
                break

            seen.add(pos)
            left_turn = (dir.ccw.apply(*pos), (n + 1), dir.ccw)
            str8_turn = (dir.apply(*pos), (n + 1), dir)

            q.appendleft(str8_turn)
            q.appendleft(left_turn)

        return coords

    coords = bfs(start, limit)
    return coords


def compute(s: str) -> int:
    lines = s.splitlines()
    num_s = lines[0]
    width = math.ceil(math.sqrt(int(num_s)))
    start = (width // 2, width // 2)

    coords = make_spiral(start=start, width=width, limit=num_s)
    if coords is not None:
        end = next(pos for pos, c in coords.items() if c == str(num_s))
    else:
        raise ValueError

    def bfs(
        start: tuple[int, int], end: tuple[int, int],
        seen: set[tuple[int, int]] | None = None,
    ) -> int:
        if seen is None:
            seen = set()
        q = deque([(start, 0)])
        min_d = 10**9
        while q:
            pos, d = q.popleft()
            if d > min_d:
                continue
            if pos in seen:
                continue
            if pos == end:
                return min(min_d, d)

            seen.add(pos)
            for adj in support.adjacent_4(*pos):
                if adj in coords:
                    q.append((adj, d + 1))
        return min_d

    return bfs(start, end)


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
