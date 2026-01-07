from __future__ import annotations

import argparse
import os.path

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


def coords_to_matrix(coords: Coords) -> np.ndarray:
    size = support.bounds(coords)[0].range.stop
    coords = dict(sorted(coords.items(), key=lambda x: (x[1], x[0])))
    return np.array([
        [1 if coords[x, y] == '#' else 0 for x in range(size)]
        for y in range(size)
    ])


def matches_rule(M: np.ndarray, R: np.ndarray) -> bool:
    orientations = [
        np.rot90(mat, k)
        for mat in (M, np.flipud(M), np.fliplr(M))
        for k in range(4)
    ]

    return any(np.array_equal(o, R) for o in orientations)


def combine(arrs: list[list[np.ndarray]]) -> np.ndarray:
    return np.vstack([np.hstack(a) for a in arrs])


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

    patterns: dict[str, np.ndarray] = {}

    def split_up(M: np.ndarray) -> list[list[np.ndarray]]:
        size = len(M)
        square = 2 if size % 2 == 0 else 3

        if size in (2, 3):
            ret = [[M]]
        else:
            ret = [
                [
                    M[i:i+square, j:j+square]
                    for j in range(0, size, square)
                ]
                for i in range(0, size, square)
            ]
        return ret

    def do(M: np.ndarray) -> np.ndarray:
        return combine([
            [new_pattern(x, rules) for x in row]
            for row in split_up(M)
        ])

    def new_pattern(
        M: np.ndarray,
        rules: list[tuple[Coords, Coords]],
    ) -> np.ndarray:
        if str(M) in patterns:
            return patterns[str(M)]
        for rule_coords, output_coords in rules:
            rule_mat = coords_to_matrix(rule_coords)
            if matches_rule(M, rule_mat):
                patterns[str(M)] = coords_to_matrix(output_coords)
                return coords_to_matrix(output_coords)
        raise ValueError

    mat = coords_to_matrix(pattern_coords)
    for _ in range(18):
        mat = do(mat)

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
