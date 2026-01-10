from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    setup_s, *states_s = s.split('\n\n')
    init_state_s, checksum_s = setup_s.splitlines()
    init_state = init_state_s[-2]
    n_steps = int(checksum_s.split()[-2])

    inst = {}

    for state_s in states_s:
        lines = state_s.splitlines()
        state = lines[0][-2]

        val_0 = int(lines[2][-2])
        move_0 = lines[3][:-1].split()[-1]
        next_state_0 = lines[4][-2]

        val_1 = int(lines[6][-2])
        move_1 = lines[7][:-1].split()[-1]
        next_state_1 = lines[8][-2]

        inst[state] = {
            0: (val_0, move_0, next_state_0),
            1: (val_1, move_1, next_state_1),
        }

    tape: dict[int, int] = {}
    pos, state = 0, init_state

    for _ in range(n_steps):
        val, move, next_state = inst[state][tape.get(pos, 0)]
        tape[pos] = val
        pos = pos + (1 if move == 'right' else -1)
        state = next_state
    return sum(tape.values())


INPUT_S = '''\
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
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
