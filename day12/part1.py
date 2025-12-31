from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
from collections import deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

graph = defaultdict(list)


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        parent_s, children_s = line.split(' <-> ')
        parent = int(parent_s)
        children = [
            x for x in map(int, children_s.split(', '))
            if x != parent
        ]
        graph[parent] = children

    end = 0

    def bfs(start: int) -> set[int]:
        q = deque([start])
        seen = set()
        while q:
            pos = q.popleft()
            if pos in seen:
                continue
            seen.add(pos)
            if pos == end:
                return seen
            for v in graph[pos]:
                if v not in seen:
                    q.append(v)
        return set()

    union = set()
    for parent in graph:
        union |= bfs(parent)

    return len(union)


INPUT_S = '''\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
'''
EXPECTED = 6


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
