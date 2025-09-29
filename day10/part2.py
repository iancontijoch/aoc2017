from __future__ import annotations

import argparse
import itertools
import os.path
from functools import reduce
from operator import xor

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


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


def compute(s: str, n_elems: int) -> str:
    s = s.strip()
    lengths = get_lengths(s)
    sparse_hash = knot_hash(s, n_elems, lengths, 64)

    dense_hash = [
        reduce(xor, sparse_hash)
        for sparse_hash in itertools.batched(sparse_hash, n=16)
    ]

    hex_str = ''.join(str.zfill(hex(x)[2:], 2) for x in dense_hash)
    return hex_str


INPUT_S = '''\
3, 4, 1, 5
'''
N_ELEMS = 256
EXPECTED = 12


@pytest.mark.parametrize(
    ('input_lst', 'input_i', 'input_window_size', 'expected'),
    (
        ([0, 1, 2, 3, 4], 0, 3, ([0, 1, 2], 0, 3)),
        ([2, 1, 0, 3, 4], 3, 4, ([3, 4, 2, 1], 3, 2)),
        ([2, 1, 0, 3, 4], 1, 4, ([1, 0, 3, 4], 1, 5)),
        ([2, 1, 0, 3, 4], 4, 5, ([4, 2, 1, 0, 3], 4, 4)),
    ),
)
def test_get_window(
    input_lst: list[int],
    input_i: int,
    input_window_size: int,
    expected: list[int],
) -> None:
    assert get_window(input_lst, input_i, input_window_size) == expected


@pytest.mark.parametrize(
    ('input_lst', 'input_i', 'input_length', 'expected'),
    (
        ([0, 1, 2, 3, 4], 0, 3, [2, 1, 0, 3, 4]),
        ([2, 1, 0, 3, 4], 3, 4, [4, 3, 0, 1, 2]),
    ),
)
def test_update_lst(
    input_lst: list[int],
    input_i: int,
    input_length: int,
    expected: list[int],
) -> None:
    assert update_lst(input_lst, input_i, input_length) == expected


@pytest.mark.parametrize(
    ('input_str', 'expected'),
    (
        ('1,2,3', [49, 44, 50, 44, 51, 17, 31, 73, 47, 23]),
    ),
)
def test_lengths(input_str: str, expected: str) -> None:
    assert get_lengths(input_str) == expected


@pytest.mark.parametrize(
    ('input_s', 'n_elems', 'expected'),
    (
        ('', N_ELEMS, 'a2582a3a0e66e6e86e3812dcb672a272'),
        ('AoC 2017', N_ELEMS, '33efeb34ea91902bb2f59c9920caa6cd'),
        ('1,2,3', N_ELEMS, '3efbe78a8d82f29979031a4aa0b16a9d'),
        ('1,2,4', N_ELEMS, '63960835bcdc130f0b66d7ff4f6a5a8e'),
    ),
)
def test(input_s: str, n_elems: int, expected: int) -> None:
    assert compute(input_s, n_elems) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read(), 256))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
