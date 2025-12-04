from datetime import datetime

from utils import run_and_submit

DIRS_DIAG = [
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
    (1, -1),
    (-1, 1),
    (-1, -1),
    (1, 1),
]


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        # lines = [list(map(int, re.findall("-?\d+", line))) for line in lines]

    return [list(line) for line in lines]


def neigh_rolls(r, c, G):
    total = 0
    for dr, dc in DIRS_DIAG:
        rr, cc = r + dr, c + dc
        if (0 <= rr < len(G)) and (0 <= cc < len(G[0])) and G[rr][cc] == "@":
            total += 1
    return total


def run(filename: str):
    G = parse(filename)

    total = 0
    for r in range(len(G)):
        for c in range(len(G[0])):
            if G[r][c] == "@" and neigh_rolls(r, c, G) < 4:
                total += 1

    return total


def runp2(filename: str):
    G = parse(filename)

    removing = True
    total_removed = 0
    while removing:
        removing = False
        to_remove = set()
        for r in range(len(G)):
            for c in range(len(G[0])):
                if G[r][c] == "@" and neigh_rolls(r, c, G) < 4:
                    total_removed += 1
                    to_remove.add((r, c))
                    removing = True
        for rr, cc in to_remove:
            G[rr][cc] = "."

    return total_removed


if __name__ == "__main__":
    day = 4
    dt = datetime(2025, 12, day)
    exp = {"a": 13, "b": None}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
