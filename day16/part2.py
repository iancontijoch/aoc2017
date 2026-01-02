from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def spin(s: str, n: int) -> str:
    if len(s) <= n:
        return s
    return s[-n:] + s[:-n]


def exchange(s: str, i: int, j: int) -> str:
    if i <= j:
        return s[:i] + s[j] + s[i+1:j] + s[i] + s[j+1:]
    else:
        return s[:j] + s[i] + s[j+1:i] + s[j] + s[i+1:]


def partner(s: str, a: str, b: str) -> str:
    return s.replace(a, 'x').replace(b, a).replace('x', b)


def parse_instr(s: str, word: str) -> str:
    if s[0] == 's':
        return spin(word, int(s[1:]))
    elif s[0] == 'x':
        a_n, b_n = map(int, s[1:].split('/'))
        return exchange(word, a_n, b_n)
    elif s[0] == 'p':
        a_s, b_s = s[1:].split('/')
        return partner(word, a_s, b_s)
    else:
        raise ValueError


def compute(s: str, word: str) -> str:
    lines = s.splitlines()
    for line in lines:
        instr_s = line.split(',')
        seen = set()
        i = 0

        def dance(word: str) -> str:
            for instr in instr_s:
                word = parse_instr(instr, word)
            return word

        start_word = word
        while True:
            word = dance(word)
            i += 1
            if word in seen:
                break
            seen.add(word)

        word = start_word
        for _ in range(1_000_000_000 % (i - 1)):
            word = dance(word)
    return word


INPUT_S = '''\
s1,x3/4,pe/b
'''
EXPECTED = 'ceadb'


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 'abcde') == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 'abcdefghijklmnop'))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
