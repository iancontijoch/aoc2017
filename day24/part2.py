from __future__ import annotations

import argparse
import os.path
from collections import deque
from typing import Deque

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Component:
    def __init__(
        self,
        id: int,
        p1: int,
        p2: int,
        p1_conn: Component | None = None,
        p2_conn: Component | None = None,
    ):
        self.id = id
        self.p1 = p1
        self.p2 = p2
        self.p1_conn = p1_conn
        self.p2_conn = p2_conn

    @property
    def ports(self) -> tuple[int, int]:
        return self.p1, self.p2

    @property
    def strength(self) -> int:
        return sum(self.ports)

    def __str__(self) -> str:
        if self.p1_conn is None and self.p2_conn is None:
            return f'{self.p1}/{self.p2}'
        elif self.p1_conn is None and self.p2_conn is not None:
            return f'{self.p1}/[{self.p2}]'
        elif self.p1_conn is not None and self.p2_conn is None:
            return f'[{self.p1}]/{self.p2}'
        else:
            return f'[{self.p1}]/[{self.p2}]'

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def connect(c1: Component, c2: Component) -> list[Component]:
        ret = []
        if c1.p1 == c2.p1 and c1.p1_conn is None and c2.p1_conn is None:
            ret.append(Component(id=c2.id, p1=c2.p1, p2=c2.p2, p1_conn=c1))
        if c1.p1 == c2.p2 and c1.p1_conn is None and c2.p2_conn is None:
            ret.append(Component(id=c2.id, p1=c2.p1, p2=c2.p2, p2_conn=c1))
        if c1.p2 == c2.p1 and c1.p2_conn is None and c2.p1_conn is None:
            ret.append(Component(id=c2.id, p1=c2.p1, p2=c2.p2, p1_conn=c1))
        if c1.p2 == c2.p2 and c1.p2_conn is None and c2.p2_conn is None:
            ret.append(Component(id=c2.id, p1=c2.p1, p2=c2.p2, p2_conn=c1))
        return ret


def compute(s: str) -> int:
    lines = s.splitlines()
    components = []
    for i, line in enumerate(lines):
        p1, p2 = map(int, line.split('/'))
        components.append(Component(id=i, p1=p1, p2=p2))

    starts = (c for c in components if c.p1 == 0 or c.p2 == 0)
    strengths = []
    for start in starts:
        q: Deque[tuple[Component, set[int], int, int]] = deque(
            [(start, set(), start.strength, 1)],
        )

        max_length = 0
        max_strength: dict[int, int] = {}
        while q:
            c1, seen, total_strength, length = q.popleft()
            if c1.id in seen:
                continue
            if length >= max_length:
                max_strength[length] = max(
                    max_strength.get(length, 0),
                    total_strength,
                )
                max_length = length
            seen.add(c1.id)
            for c2 in (
                c for c in components
                if c.id != c1.id and c.id not in seen
                and 0 not in c.ports
            ):
                for conn in Component.connect(c1, c2):
                    q.append((
                        conn,
                        seen.copy(),
                        total_strength + c2.strength,
                        length + 1,
                    ))
        strengths.append(max(max_strength.items()))
    return max(strengths)[1]


INPUT_S = '''\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
'''
EXPECTED = 19


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
