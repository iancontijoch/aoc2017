from __future__ import annotations

import argparse
import itertools
import os.path
from collections import deque
from functools import reduce
from operator import xor

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
N_ELEMS = 256


def get_window(
    lst: list[int],
    i: int, window_size: int,
) -> tuple[list[int], int, int]:
    lst_len = len(lst)
    window_end = i + window_size
    if window_end > lst_len:
        window_start, window_end = i, window_end - lst_len
        right = lst[window_start:]
        left = lst[:window_end]
        return (right + left, window_start, window_end)
    return (lst[i:window_end], i, window_end)


def update_lst(lst: list[int], i: int, length: int) -> list[int]:
    # get reversed window
    window, window_start, window_end = get_window(lst, i, length)
    reversed_window = window[::-1]

    # window is zero, return list as-is
    if length == 0:
        # plus do stuff
        return lst
    # 2. if window end > window start, no wrap-around
    if window_end > window_start:
        return lst[:window_start] + reversed_window + lst[window_end:]
    elif window_end <= window_start:
        same = lst[window_end:i]
        left = reversed_window[-window_end:]
        right = reversed_window[:-window_end]
        return left + same + right
    else:
        raise ValueError


def get_lengths(s: str) -> list[int]:
    return [ord(x) for x in s] + [17, 31, 73, 47, 23]


def knot_hash(
    s: str, n_elems: int,
    lengths: list[int], rounds: int,
) -> list[int]:
    lst = list(range(n_elems))
    len_lst = len(lst)
    i = skip_size = 0

    for _ in range(rounds):
        for n in lengths:
            lst = update_lst(lst, i, n)
            i = (i + n + skip_size) % len_lst
            skip_size += 1
    return lst


def compute_hash(s: str, n_elems: int) -> str:
    s = s.strip()
    lengths = get_lengths(s)
    sparse_hash = knot_hash(s, n_elems, lengths, 64)

    dense_hash = [
        reduce(xor, sparse_hash)
        for sparse_hash in itertools.batched(sparse_hash, n=16)
    ]

    hex_str = ''.join(str.zfill(hex(x)[2:], 2) for x in dense_hash)
    return hex_str


def hash_to_hex(s: str) -> list[int]:
    ret = list(map(int, ''.join(bin(int(c, 16))[2:].zfill(4) for c in s)))
    return ret


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    rows = []
    for line in lines:
        for i in range(128):
            hash_s = compute_hash(f'{line.strip()}-{i}', N_ELEMS)
            hex_s = hash_to_hex(hash_s)
            rows.append(hex_s)

    coords = {
        (x, y): val
        for x, row in enumerate(rows)
        for y, val in enumerate(row)
    }

    seen = set()

    def bfs(start: tuple[int, int]) -> set[tuple[int, int]]:
        q = deque([start])
        seen_region = set()
        while q:
            pos = q.popleft()
            if pos in seen_region:
                continue
            seen_region.add(pos)
            for adj in support.adjacent_4(*pos):
                if (
                    adj not in seen_region
                    and adj in coords
                    and coords[adj] == 1
                ):
                    q.append(adj)
        return seen_region

    for pos in coords:
        if pos not in seen and coords[pos] == 1:
            region = bfs(pos)
            seen |= region
            total += 1

    return total


INPUT_S = '''\
flqrgnkx
'''
EXPECTED = 1242


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
