from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
AXIAL_COORDS: dict[str, tuple[int, int, int]] = {
    'n': (0, -1, 1),
    'ne': (1, -1, 0),
    'se': (1, 0, -1),
    's': (0, 1, -1),
    'sw': (-1, 1, 0),
    'nw': (-1, 0, 1),
}


def move(pos: tuple[int, int, int], dir: str) -> tuple[int, int, int]:
    delta = AXIAL_COORDS.get(dir)
    if delta is None:
        raise ValueError

    pq, pr, ps = pos
    dq, dr, ds = delta

    return (pq + dq, pr + dr, ps + ds)


def dist(h1: tuple[int, int, int], h2: tuple[int, int, int]) -> int:
    h1q, h1r, h1s = h1
    h2q, h2r, h2s = h2
    v1q, v1r, v1s = (h2q - h1q, h2r - h1r, h2s - h1s)
    return max(abs(v1q), abs(v1r), abs(v1s))


def compute(s: str) -> int:
    line = s.splitlines()[0]
    moves = line.split(',')
    start = pos = (0, 0, 0)
    max_d = 0
    for m in moves:
        pos = move(pos, m)
        max_d = max(max_d, dist(start, pos))
    return max_d


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('ne,ne,ne', 3),
        ('ne,ne,sw,sw', 2),
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
