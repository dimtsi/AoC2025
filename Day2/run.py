from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().replace("\n", "").split(",")

    out = []
    for line in lines:
        out.append([int(x) for x in line.split("-")])
    return out


def check_corr(num):
    n = str(num)

    l = len(n)
    if l % 2:
        return False
    if n[: len(n) // 2] == n[(len(n) // 2) :]:
        return True
    return False


def check_corr_2(num):
    n = str(num)
    l = len(n)
    for i in range(1, l):
        s = n[:i]
        j = i
        while j < len(n):
            if n[j : j + i] == s:
                j += i
            else:
                break
        else:
            return True
    return False


def run(filename: str, p2=False):
    lines = parse(filename)
    total = 0

    f = check_corr if not p2 else check_corr_2

    for a, b in lines:
        for i in range(a, b + 1):
            if f(i):
                total += i

    return total


def runp2(filename: str):
    return run(filename, p2=True)


if __name__ == "__main__":
    day = 2
    dt = datetime(2025, 12, day)
    exp = {"a": 1227775554, "b": 4174379265}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
