import re
from datetime import datetime
from functools import reduce

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        L = len(lines)
        nums, ops = lines[: L - 1], lines[L - 1]
        nums = [list(map(int, re.findall(r"-?\d+", line.strip()))) for line in nums]
        ops = re.sub(r"\s+", " ", ops).split(" ")

    return nums, ops


def run(filename: str):
    nums, ops = parse(filename)
    totals = nums[0]

    for line in nums[1:]:
        for (i, n), op in zip(enumerate(line), ops):
            if op == "*":
                totals[i] *= n
            elif op == "+":
                totals[i] += n
            else:
                raise Exception(f"Unknown op {op}")

    return sum(totals)


def calc_p2(nums, op):
    out = ["" for _ in range(len(nums[0]))]

    for n in nums:
        for i, c in enumerate(n):
            if c != " ":
                out[i] += c

    ints = [int(x.strip()) for x in out]

    if op == "*":
        return reduce(lambda x, y: x * y, ints)
    elif op == "+":
        return reduce(lambda x, y: x + y, ints)
    else:
        raise Exception("wrong op")


def parse2(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        L = len(lines)

        last = lines[-1]
        ops = re.sub(r"\s+", " ", last).split(" ")
        out = []

        empty = []
        for i in range(len(last)):
            if last[i] in "+*" and i > 0:
                empty.append(i - 1)

        for row in lines[:-1]:
            l = []
            curr = ""
            for i, c in enumerate(row):
                if i in empty:
                    l.append(curr)
                    curr = ""
                    continue
                curr += c
            l.append(curr)
            out.append(l[:])

    return out, ops


def runp2(filename: str):
    nums, ops = parse2(filename)

    total = 0
    for i in range(len(nums[0])):
        col = [nums[row][i] for row in range(len(nums))]
        total += calc_p2(col, ops[i])

    return total


if __name__ == "__main__":
    day = 6
    dt = datetime(2025, 12, day)
    exp = {"a": 4277556, "b": 3263827}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
