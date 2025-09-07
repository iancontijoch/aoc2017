from __future__ import annotations

import argparse
import operator
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OPS = {
    'inc': operator.add,
    'dec': operator.sub,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '<': operator.lt,
    '>=': operator.ge,
    '>': operator.gt,
}


def compute(s: str) -> int:
    lines = s.splitlines()
    regs = {}

    # first pass to get register vals
    for line in lines:
        x, _, _, _, y, *_ = line.split()
        if x not in regs:
            regs[x] = 0
        if y not in regs:
            regs[y] = 0

    for line in lines:
        x, op_s, n_s, _, y, cmp_s, cmp_n_s = line.split()
        op, cmp = OPS[op_s], OPS[cmp_s]
        if cmp(regs[y], int(cmp_n_s)):
            regs[x] = op(regs[x], int(n_s))

    return max(regs.values())


INPUT_S = '''\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
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
