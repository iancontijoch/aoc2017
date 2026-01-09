from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from collections.abc import Callable

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    instrs = [line.split() for line in lines]

    reg: dict[str, int] = defaultdict(int)
    pos = 0

    def value(s: str) -> int:
        return int(s) if s.isdigit() or s.startswith('-') else reg[s]

    def set(x: str, y: str, pos: int) -> int:
        reg[x] = value(y)
        return pos + 1

    def add(x: str, y: str, pos: int) -> int:
        reg[x] += value(y)
        return pos + 1

    def sub(x: str, y: str, pos: int) -> int:
        reg[x] -= value(y)
        return pos + 1

    def mul(x: str, y: str, pos: int) -> int:
        reg[x] *= value(y)
        return pos + 1

    def jnz(x: str, y: str, pos: int) -> int:
        if value(x) != 0:
            return pos + value(y)
        else:
            return pos + 1

    funcs: dict[str, Callable[..., int]] = {
        'set': set,
        'add': add,
        'sub': sub,
        'mul': mul,
        'jnz': jnz,
    }

    def parse_instr(instr: list[str]) -> int:
        try:
            return funcs[instr[0]](*instr[1:], pos)
        except ValueError:
            raise

    while pos < len(instrs):
        curr_instr = instrs[pos]
        # print(curr_instr)
        if curr_instr[0] == 'mul':
            total += 1
        pos = parse_instr(curr_instr)

    # print(reg)
    return total


INPUT_S = '''\
'''
EXPECTED = 1


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
