import itertools
import re
from collections import defaultdict
from datetime import datetime
from functools import reduce

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [list(map(int, re.findall(r"\d+", line))) for line in lines]
    return lines


def dist(a, b):
    ax, ay, az = a
    bx, by, bz = b
    return (abs(ax - bx) ** 2) + (abs(ay - by) ** 2) + (abs(az - bz) ** 2)


def simulate(P, p2=False, sample=False):
    dists = []
    for a, b in itertools.combinations(P, 2):
        dists.append([tuple(a), tuple(b), dist(a, b)])

    M = {}
    g_idx = 0
    SD = sorted(dists, key=lambda x: x[2])
    if not p2:
        SD = SD[: (10 if sample else 1000)]
    for a, b, _ in SD:
        if a not in M and b not in M:
            M[a] = M[b] = g_idx
            g_idx += 1
            last = a, b

        elif (a in M) ^ (b in M):
            group = M[a] if a in M else M[b]
            M[a] = M[b] = group
            last = a, b

        elif (a in M) and (b in M):
            if M[a] == M[b]:
                continue
            else:
                group_a = M[a]
                group_b = M[b]
                for k, v in M.items():
                    if v == group_b:
                        M[k] = group_a
                last = a, b
        else:
            raise Exception("Unknown case")

    if not p2:
        sizes = defaultdict(int)
        for _, g in M.items():
            sizes[g] += 1

        lens = sorted(sizes.values(), reverse=True)[:3]
        score = reduce(lambda x, y: x * y, lens)
        return score
    else:
        return last[0][0] * last[1][0]


def run(filename: str, p2=False):
    P = parse(filename)
    sample = "sample" in filename
    score = simulate(P, p2, sample)
    return score


def runp2(filename: str):
    return run(filename, True)


if __name__ == "__main__":
    day = 8
    dt = datetime(2025, 12, day)
    exp = {"a": 40, "b": 25272}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
