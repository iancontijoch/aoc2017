from __future__ import annotations

import argparse
import os.path
from dataclasses import dataclass

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


@dataclass
class Program():
    name: str
    weight: int
    children: list[str] | None = None
    root: str | None = None


def compute(s: str) -> str:
    lines = s.splitlines()
    programs: dict[str, Program] = {}
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            program_name, weight_s = parts
            children = None
        else:
            program_s, children_s = line.split(' -> ')
            program_name, weight_s = program_s.split()
            children = children_s.split(', ')

        weight = int(weight_s[1:-1])
        programs[program_name] = Program(program_name, weight, children)

    for name, prog in programs.items():
        if prog.children is not None:
            for child in prog.children:
                if child in programs:
                    programs[child].root = name

    return next(k for k, v in programs.items() if v.root is None)


INPUT_S = '''\
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
'''
EXPECTED = 'tknk'


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
