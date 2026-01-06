from __future__ import annotations

import argparse
import os.path
from collections.abc import Sequence

import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

Coords = dict[tuple[int, int], str]


def rule_to_coords(s: str) -> Coords:
    coords = {
        (x, y): c
        for y, line in enumerate(s.split('/'))
        for x, c in enumerate(line)
    }
    return coords


def remove_oob(coords: Coords) -> Coords:
    return {(x, y): c for (x, y), c in coords.items() if x >= 0 and y >= 0}


def coords_to_matrix(coords: Coords) -> np.ndarray:
    size = support.bounds(coords)[0].range.stop
    coords = dict(sorted(coords.items(), key=lambda x: (x[1], x[0])))
    return np.array([
        [1 if coords[x, y] == '#' else 0 for x in range(size)]
        for y in range(size)
    ])


def matches_rule(m: np.ndarray, r: np.ndarray) -> bool:
    orientations = [
        np.rot90(mat, k)
        for mat in (m, np.flipud(m), np.fliplr(m))
        for k in range(4)
    ]

    return any(np.array_equal(o, r) for o in orientations)


def new_pattern(
    m: np.ndarray,
    rules: list[tuple[Coords, Coords]],
) -> np.ndarray:
    for rule_coords, output_coords in rules:
        rule_mat = coords_to_matrix(rule_coords)
        if matches_rule(m, rule_mat):
            return coords_to_matrix(output_coords)
    raise ValueError


def split_up(M: np.ndarray) -> list[np.ndarray]:
    size = len(M)
    if size in (2, 3):
        return [M]
    elif size % 2 == 0:
        return [
            M[i:i+2, j:j+2]
            for i in range(0, size, 2)
            for j in range(0, size, 2)
        ]
    elif size % 3 == 0:
        span = size // 3
        qs = [
            M[:span, :span],
            M[:span, span:2*span],
            M[:span, 2*span:],
            M[span:2*span, :span],
            M[span:2*span, span:2*span],
            M[span:2*span, 2*span:],
            M[2*span:, :span],
            M[2*span:, span:2*span],
            M[2*span:, 2*span:],
        ]
        return qs
    else:
        raise NotImplementedError


def combine(arrs: Sequence[np.ndarray]) -> np.ndarray:
    if len(arrs) == 1:
        return arrs[0]
    elif len(arrs) % 2 == 0:
        mid = len(arrs) // 2
        return np.vstack((np.hstack(arrs[:mid]), np.hstack(arrs[mid:])))
    elif len(arrs) == 9:
        return np.vstack((
            np.hstack(arrs[:3]),
            np.hstack(arrs[3:6]),
            np.hstack(arrs[6:]),
        ))
    else:
        raise ValueError


def compute(s: str) -> int:
    lines = s.splitlines()
    pattern = '.#.\n..#\n###'

    pattern_coords = {
        (x, y): c
        for y, line in enumerate(pattern.splitlines())
        for x, c in enumerate(line)
    }
    rules = []

    for line in lines:
        rule_from, rule_to = line.split(' => ')
        rule_coords = rule_to_coords(rule_from)
        output_coords = rule_to_coords(rule_to)

        rules.append((rule_coords, output_coords))

    mat = coords_to_matrix(pattern_coords)
    mats = [mat]

    for _ in range(5):
        mats = [
            combine(
                [new_pattern(m, rules) for m in split_up(mat)],
            ) for mat in mats
        ]
    mat = combine(mats)
    return int(np.sum(mat))


INPUT_S = '''\
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
'''

EXPECTED = 12


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
