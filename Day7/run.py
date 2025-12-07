from copy import deepcopy
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]
    print(lines)
    return lines


def find_start_splits(G):
    start = None
    splits = []
    for i in range(len(G)):
        row_spl = []
        for j in range(len(G[0])):
            if G[i][j] == "S":
                start = (i, j)
            if G[i][j] == "^":
                row_spl.append((i, j))
        splits.append(row_spl)
    return start, splits


def simulate(splits, start):
    b = {start[1]}
    i = 0
    total = 0
    while i < len(splits):
        next_b = deepcopy(b)
        for _, tc in splits[i]:
            for bc in b:
                if tc == bc:
                    next_b.remove(bc)
                    next_b |= {tc - 1, tc + 1}
                    total += 1

        b = next_b
        i += 1
    return total


def run(filename: str):
    G = parse(filename)
    start, SPL = find_start_splits(G)
    out = simulate(SPL, start)
    return out


def simulate2(G, start):
    cache = {}

    def dfs(r, c):
        if r == len(G[0]):
            return 1

        if (r, c) in cache:
            return cache[(r, c)]

        total = 0
        if G[r][c] == "^":
            total += dfs(r + 1, c - 1)
            total += dfs(r + 1, c + 1)
        else:
            total += dfs(r + 1, c)

        cache[(r, c)] = total
        return total

    return dfs(*start)


def runp2(filename: str):
    G = parse(filename)
    start, _ = find_start_splits(G)
    out = simulate2(G, start)
    return out


if __name__ == "__main__":
    day = 7
    dt = datetime(2025, 12, day)
    exp = {"a": 21, "b": 40}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
