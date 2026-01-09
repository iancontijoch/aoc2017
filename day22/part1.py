from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, n_bursts: int) -> int:
    lines = s.splitlines()
    total = 0

    coords = {
        (x, y): c
        for y, line in enumerate(lines)
        for x, c in enumerate(line)
    }

    bx, by = support.bounds(coords)
    mid = (bx.max // 2, by.max // 2)

    pos, d = (mid, support.Direction4.UP)

    for _ in range(n_bursts):
        c = coords.get(pos, '.')
        d = d.cw if c == '#' else d.ccw
        if c == '.':
            coords[pos] = '#'
            total += 1
        else:
            coords[pos] = '.'
        pos = support.Direction4.apply(d, *pos)
    return total


INPUT_S = '''\
..#
#..
...
'''

N_BURSTS_1 = 7
EXPECTED_1 = 5

N_BURSTS_2 = 70
EXPECTED_2 = 41

N_BURSTS_3 = 10000
EXPECTED_3 = 5587


@pytest.mark.parametrize(
    ('input_s', 'n_bursts', 'expected'),
    (
        (INPUT_S, N_BURSTS_1, EXPECTED_1),
        (INPUT_S, N_BURSTS_2, EXPECTED_2),
        (INPUT_S, N_BURSTS_3, EXPECTED_3),
    ),
)
def test(input_s: str, n_bursts: int, expected: int) -> None:
    assert compute(input_s, n_bursts) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 10000))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
