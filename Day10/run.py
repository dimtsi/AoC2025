import re
from datetime import datetime
from heapq import heapify, heappop

from z3.z3 import *

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lights = [list(re.findall(r"\[.*\]", line))[0][1:-1] for line in lines]
        wires = [list(re.findall(r"\(.*\)", line))[0] for line in lines]
        W = []
        for wire in wires:
            lw = []
            groups = wire.split(" ")
            for group in groups:
                lw.append(tuple(map(int, re.findall(r"\d+", group))))
            W.append(lw)

        jolt = [list(re.findall(r"\{.*\}", line))[0] for line in lines]

        j = [(tuple(map(int, re.findall(r"\d+", j)))) for j in jolt]

    return lights, W, j


def find(L, B):
    L = set(L)
    B = set(B)

    pq = [(1, set(btn)) for btn in B]
    heapify(pq)
    visited = set()

    while pq:
        d, curr = heappop(pq)

        key = frozenset(curr)
        if key in visited:
            continue

        visited.add(key)

        if curr == L:
            return d

        for button in B:
            pq.append((d + 1, curr ^ set(button)))
    return float("inf")


def run(filename: str):
    L, W, J = parse(filename)

    LL = []
    for lights in L:
        l = [i for i, c in enumerate(lights) if c == "#"]
        LL.append(tuple(l))

    total = 0
    for lights, wires, _ in zip(LL, W, J):
        total += find(lights, wires)

    return total


def findp2(B, J):
    o = Optimize()

    presses = [Int(f"n{i}") for i in range(len(B))]

    for press in presses:
        o.add(press >= 0)

    for i, target in enumerate(J):
        expr = []
        for j, button in enumerate(B):
            for b in button:
                if b == i:
                    expr.append(presses[j])
        o.add((Sum(expr)) == target)

    objective = Sum(presses)
    o.minimize(objective)

    res = o.check()
    assert res == sat
    m = o.model()

    out_presses = [m[x].as_long() for x in presses]
    return sum(out_presses)


def runp2(filename: str):
    _, W, J = parse(filename)

    total = 0
    for wires, jolts in zip(W, J):
        total += findp2(wires, jolts)

    return total


if __name__ == "__main__":
    day = 10
    dt = datetime(2025, 12, day)
    exp = {"a": 7, "b": 33}
    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
