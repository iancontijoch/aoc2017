from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from collections import deque
from collections.abc import Callable
from typing import Deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    instrs = [line.split() for line in lines]
    total = 0

    last_sound = 0
    reg0: dict[str, int] = defaultdict(int)
    reg1: dict[str, int] = defaultdict(int)

    reg1['p'] = 1

    pos0, pos1 = 0, 0
    q0: Deque[int] = deque([])
    q1: Deque[int] = deque([])

    def value(s: str, reg_n: int) -> int:
        reg = reg0 if reg_n == 0 else reg1
        return int(s) if s.isdigit() or s.startswith('-') else reg[s]

    def snd(x: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        receive_q = q1 if reg_n == 0 else q0
        val = value(x, reg_n)
        receive_q.append(val)
        return pos + 1, last_sound

    def set(x: str, y: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        reg = reg0 if reg_n == 0 else reg1
        reg[x] = value(y, reg_n)
        return pos + 1, None

    def add(x: str, y: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        reg = reg0 if reg_n == 0 else reg1
        reg[x] += value(y, reg_n)
        return pos + 1, None

    def mul(x: str, y: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        reg = reg0 if reg_n == 0 else reg1
        reg[x] *= value(y, reg_n)
        return pos + 1, None

    def mod(x: str, y: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        reg = reg0 if reg_n == 0 else reg1
        reg[x] %= value(y, reg_n)
        return pos + 1, None

    def rcv(x: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        receive_reg = reg0 if reg_n == 0 else reg1
        q = q0 if reg_n == 0 else q1
        if q:
            receive_reg[x] = q.popleft()
            return pos + 1, None
        return pos, None

    def jgz(x: str, y: str, pos: int, reg_n: int) -> tuple[int, int | None]:
        if value(x, reg_n) > 0:
            return pos + value(y, reg_n), None
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

    def parse_instr(instr: list[str], reg_n: int) -> tuple[int, int | None]:
        pos = pos0 if reg_n == 0 else pos1
        try:
            return funcs[instr[0]](*instr[1:], pos, reg_n)
        except ValueError:
            raise

    while pos0 < len(instrs) and pos1 < len(instrs):
        curr_instr_0 = instrs[pos0]
        curr_instr_1 = instrs[pos1]

        pos0, _ = parse_instr(curr_instr_0, 0)
        pos1, _ = parse_instr(curr_instr_1, 1)

        if curr_instr_1[0] == 'snd':
            total += 1
        if (
            (curr_instr_0[0] == 'rcv' and curr_instr_1[0] == 'rcv')
            and not q0 and not q1
        ):
            break
    return total


INPUT_S = '''\
snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d
'''
EXPECTED = 3


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
