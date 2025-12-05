import re
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        ranges, ingr = f.read().strip().split("\n\n")
        ranges = [
            list(map(int, re.findall(r"\d+", line))) for line in ranges.split("\n")
        ]
        ingr = [int(x) for x in ingr.split("\n")]
    return (ranges, ingr)


def run(filename: str):
    ranges, ingr = parse(filename)

    total = 0
    for ing in ingr:
        for s, e in ranges:
            if s <= ing <= e:
                total += 1
                break
    return total


def merge_intervals(ivs):
    ivs.sort()
    m = []

    for s, e in ivs:
        if m and m[-1][1] >= s:
            m[-1][1] = max(m[-1][1], e)
        else:
            m.append([s, e])
    return m


def runp2(filename: str):
    ranges, _ = parse(filename)

    ivs = merge_intervals(ranges)

    total = 0
    for s, e in ivs:
        total += (e - s) + 1

    return total


if __name__ == "__main__":
    day = 5
    dt = datetime(2025, 12, day)
    exp = {"a": 3, "b": 14}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
