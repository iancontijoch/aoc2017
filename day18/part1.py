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
    instrs = [line.split() for line in lines]

    last_sound = 0
    reg: dict[str, int] = defaultdict(int)
    pos = 0

    def value(s: str) -> int:
        return int(s) if s.isdigit() or s.startswith('-') else reg[s]

    def snd(x: str, pos: int) -> tuple[int, int | None]:
        last_sound = value(x)
        return pos + 1, last_sound

    def set(x: str, y: str, pos: int) -> tuple[int, int | None]:
        reg[x] = value(y)
        return pos + 1, None

    def add(x: str, y: str, pos: int) -> tuple[int, int | None]:
        reg[x] += value(y)
        return pos + 1, None

    def mul(x: str, y: str, pos: int) -> tuple[int, int | None]:
        reg[x] *= value(y)
        return pos + 1, None

    def mod(x: str, y: str, pos: int) -> tuple[int, int | None]:
        reg[x] %= value(y)
        return pos + 1, None

    def rcv(x: str, pos: int) -> tuple[int, int | None]:
        if value(x) != 0:
            return pos + 1, last_sound
        return pos + 1, None

    def jgz(x: str, y: str, pos: int) -> tuple[int, int | None]:
        if value(x) > 0:
            return pos + value(y), None
        else:
            return pos + 1, None

    funcs: dict[str, Callable[..., tuple[int, int | None]]] = {
        'set': set,
        'add': add,
        'mul': mul,
        'mod': mod,
        'jgz': jgz,
        'rcv': rcv,
        'snd': snd,
    }

    def parse_instr(instr: list[str]) -> tuple[int, int | None]:
        try:
            return funcs[instr[0]](*instr[1:], pos)
        except ValueError:
            raise

    while pos < len(instrs):
        curr_instr = instrs[pos]
        pos, sound = parse_instr(curr_instr)
        if sound is not None:
            if curr_instr[0] == 'snd':
                last_sound = sound
            elif curr_instr[0] == 'rcv':
                return sound
            else:
                raise ValueError
    return 0


INPUT_S = '''\
set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2
'''
EXPECTED = 4


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
