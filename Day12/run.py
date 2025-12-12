import re
from datetime import datetime

import numpy as np

from utils import run_and_submit

KSIZE = 3


def parse(filename: str):
    T = []
    R = []
    with open(filename, "r") as f:
        segments = f.read().strip().split("\n\n")
        tiles, rules = segments[:-1], segments[-1]

    for tile in tiles:
        tile = np.array(tile.split("\n")[1:])
        T.append(to_int(tile))

    for rule in rules.split("\n"):
        dims, needs = rule.split(": ")
        dims = list(map(int, re.findall(r"\d+", dims)))
        needs = list(map(int, re.findall(r"\d+", needs)))
        R.append([dims, needs])

    return np.array(T), R


def to_int(kernel):
    return np.array(
        [
            [0 if kernel[i][j] != "#" else 1 for j in range(len(kernel[0]))]
            for i in range(len(kernel))
        ]
    )


#
#
# def O(tile):
#     result = []
#     for k in range(4):
#         a = np.rot90(tile, k)
#         result.append(a)
#         result.append(np.fliplr(a))
#     return result
#
#
# def get_next(expected):
#     for i in range(len(expected)):
#         if expected[i] != 0:
#             return i
#
#
# def overlaps(G, tile, r, c):
#     slice = G[r : r + KSIZE, c : c + KSIZE]
#     return np.any(slice & tile)
#
#
# def fit(T, rule):
#     dim, expected = rule
#     C, R = dim
#     OG = np.zeros((dim[::-1]), dtype=int)
#
#     start = get_next(expected)
#
#     starts = []
#     for r in range(R - 2):
#         for c in range(C - 2):
#             for orientation in O(T[start]):
#                 SG = OG.copy()
#                 SG[r : r + 3, c : c + 3] = orientation
#                 starts.append((SG, expected[:]))
#
#     q = deque(starts)
#     visited = set()
#
#     while q:
#         G, rem = q.pop()
#         key = (G.tobytes(), tuple(rem))
#
#         if key in visited:
#             # print("key")
#             continue
#
#         if sum(rem) == 0:
#             return True
#
#         visited.add(key)
#
#         next_ = get_next(rem)
#         next_rem = rem[:]
#         next_rem[next_] -= 1
#
#         for r in range(R - 2):
#             for c in range(C - 2):
#                 for orientation in O(T[next_]):
#                     if G[r][c] == 0 and not overlaps(G, orientation, r, c):
#                         # print("==========")
#                         # print(G)
#                         # print(r, c)
#                         # print(orientation)
#                         NG = G.copy()
#                         NG[r : r + 3, c : c + 3] = orientation + G[r : r + 3, c : c + 3]
#                         # print(NG)
#                         # print("=====")
#                         q.append((NG, next_rem[:]))
#     return False


def check_if_possible_by_area(T, rule):
    sizes = [np.sum(tile).item() for i, tile in enumerate(T)]
    dim, expected = rule
    area = dim[0] * dim[1]

    needed = sum(size * n for size, n in zip(sizes, expected))
    return area >= 1.2 * needed


def run(filename: str):
    T, R = parse(filename)
    print(T)
    total = 0
    for i, rule in enumerate(R):
        total += int(check_if_possible_by_area(T, rule))
    return total


def runp2(filename: str):
    return run(filename)


if __name__ == "__main__":
    day = 12
    dt = datetime(2025, 12, day)
    exp = {"a": 2, "b": False}

    # run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
