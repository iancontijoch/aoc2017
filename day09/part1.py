from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def nullify_s(s: str) -> str:
    pattern = r'!.'
    return ''.join(re.split(pattern, s))


def remove_garbage(s: str) -> str:
    s = nullify_s(s)
    pattern = r'<>|<.+?>'
    ret = ''.join(re.split(pattern, s))
    ret = ''.join(re.split(r',{2,}', ret))
    return ret


def n_groups(s: str) -> int:
    s = remove_garbage(s)
    left_brackets = s.count('{')
    right_brackets = s.count('}')
    return left_brackets if left_brackets == right_brackets else 0


def is_nested(s: str) -> bool:
    return len(s) > 2 and (s[0] == '{' and s[1] != '}')


def score(s: str) -> int:
    n = total = 0
    left_brackets: list[int] = []
    for c in s:
        if not left_brackets:
            left_brackets.append(1)
            continue
        if c == '{':
            left_brackets.append(left_brackets[-1] + 1)
            n += 1
        if c == '}':
            total += left_brackets.pop()
    return total


def compute(s: str) -> int:
    lines = s.splitlines()
    return sum(score(remove_garbage(line)) for line in lines)


INPUT_S = """\

"""
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('{}', '{}'),
        ('{{{}}}', '{{{}}}'),
        ('{{},{}}', '{{},{}}'),
        ('{{{},{},{{}}}}', '{{{},{},{{}}}}'),
        ('{<{},{},{{}}>}', '{}'),
        ('{<a>,<a>,<a>,<a>}', '{}'),
        ('{{<a>},{<a>},{<a>},{<a>}}', '{{},{},{},{}}'),
        ('{{<!>},{<!>},{<!>},{<a>}}', '{{}}'),
        ('{{<!!>},{<!!>},{<!!>},{<!!>}}', '{{},{},{},{}}'),
        ('{<o!!u!"<!>}', '{<ou<}'),
        ('{<,>}', '{}'),
        ('<>', ''),
        ('<random characters>', ''),
        ('<<<<>', ''),
        ('<{!>}>', ''),
        ('<!!>', ''),
        ('<!!!>>', ''),
        ('<{o"i!a,<{i<a>', ''),
    ),
)
def test_remove_garbage(input_s: str, expected: str) -> None:
    assert remove_garbage(input_s) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('{}', 1),
        ('{{}}', 2),
        ('{{{}}}', 3),
        ('{{},{}}', 3),
        ('{{{},{},{{}}}}', 6),
        ('{<{},{},{{}}>}', 1),
        ('{<a>,<a>,<a>,<a>}', 1),
        ('{{<a>},{<a>},{<a>},{<a>}}', 5),
        ('{{<!>},{<!>},{<!>},{<a>}}', 2),
    ),
)
def test_n_groups(input_s: str, expected: int) -> None:
    assert n_groups(input_s) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('{}', False),
        ('{{{}}}', True),
        ('{{},{}}', True),
        ('{{{},{},{{}}}}', True),
        ('{{}}', True),
        ('{{}, {}}', True),
        ('{}, {}', False),
        ('{,{}}', True),
        ('{o{}}', True),
    ),
)
def test_is_nested(input_s: str, expected: int) -> None:
    assert is_nested(input_s) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('{}', '{}'),
        ('{{<!>},{<!>},{<!>},{<a>}}', '{{<},{<},{<},{<a>}}'),
        ('{<!><!><!>}', '{<<<}'),
        ('{!<><!><!>}', '{><<}'),
        ('{!!<}', '{<}'),
        ('{<o!!u!"<!>}', '{<ou<}'),
    ),
)
def test_nullify_s(input_s: str, expected: int) -> None:
    assert nullify_s(input_s) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('', 0),
        ('{<}>}', 1),
        ('{}', 1),
        ('{{{}}}', 6),
        ('{{},{}}', 5),
        ('{{{},{},{{}}}}', 16),
        ('{<a>,<a>,<a>,<a>}', 1),
        ('{{<a>},{<a>},{<a>},{<a>}}', 9),
        ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
        ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
        ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
        ('{{}}', 3),
        ('{,{}}', 3),
        ('{{,{}},{}}', 8),
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
