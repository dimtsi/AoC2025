import itertools
import re
from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")
        lines = [tuple(map(int, re.findall(r"-?\d+", line))) for line in lines]
    return lines


def edge_overlaps(minx, maxx, miny, maxy, eminx, eminy, emaxx, emaxy):
    # vertical edge
    if eminx == emaxx:
        x = eminx
        if not (minx < x < maxx):
            return False
        return max(eminy, miny) < min(emaxy, maxy)

    # horizontal edge
    elif eminy == emaxy:
        y = eminy
        if not (miny < y < maxy):
            return False
        return max(eminx, minx) < min(emaxx, maxx)

    else:
        raise ValueError("Not straight lines")


def run(filename: str, p2=False):
    P = parse(filename)

    best = 0
    for a, b in itertools.combinations(P, 2):
        ax, ay = a
        bx, by = b

        minx, maxx = min(ax, bx), max(ax, bx)
        miny, maxy = min(ay, by), max(ay, by)

        if not p2:
            best = max(best, (maxx - minx + 1) * (maxy - miny + 1))
        else:
            # edges
            for i, u in enumerate(P):
                ux, uy = u
                j = i + 1 if i < len(P) - 1 else 0
                v = P[j]
                vx, vy = v
                if {u, v} == {a, b}:
                    continue

                eminx, eminy = min(ux, vx), min(uy, vy)
                emaxx, emaxy = max(ux, vx), max(uy, vy)
                if edge_overlaps(minx, maxx, miny, maxy, eminx, eminy, emaxx, emaxy):
                    break

            else:
                best = max(best, (maxx - minx + 1) * (maxy - miny + 1))

    return best


def runp2(filename: str):
    return run(filename, p2=True)


if __name__ == "__main__":
    day = 9
    dt = datetime(2025, 12, day)
    exp = {"a": 50, "b": 24}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
