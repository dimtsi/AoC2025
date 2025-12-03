from collections import defaultdict, deque
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [[int(x) for x in line] for line in lines]
    return lines


def sim(num):
    best = 0
    for i in range(len(num)):
        for j in range(i + 1, len(num)):
            n = int(str(num[i]) + str(num[j]))
            best = max(n, best)
    return best


def sim2(num):
    G = defaultdict(deque)
    for i, d in enumerate(num):
        G[d].append(i)

    best = []

    min_idx = 0
    rem = 12
    while rem > 0:
        for d in range(9, -1, -1):
            while G[d] and G[d][0] < min_idx:
                G[d].popleft()

            if not G[d]:
                continue

            idx = G[d][0]
            if len(num) - idx < rem:  # Cannot reach 12
                continue

            min_idx = G[d].popleft()
            best.append(d)
            rem -= 1
            break
    return int("".join([str(d) for d in best]))


def run(filename: str, p2=False):
    f = sim2 if p2 else sim
    lines = parse(filename)
    total = 0
    for row in lines:
        n = f(row)
        total += n

    return total


def runp2(filename):
    return run(filename, p2=True)


if __name__ == "__main__":
    day = 3
    dt = datetime(2025, 12, day)
    exp = {"a": 0, "b": 3121910778619}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
