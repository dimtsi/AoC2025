from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    out = []
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

        for line in lines:
            move, num = line[0], int(line[1:])
            out.append((move, num))

    return out


def run(filename: str):
    lines = parse(filename)

    n = 50
    pwd = 0

    for move, num in lines:
        if move == "R":
            n = (n + num) % 100
        else:
            n = (n - num) % 100
        if n == 0:
            pwd += 1
    return pwd


def runp2(filename: str):
    lines = parse(filename)

    n = 50
    pwd = 0

    for move, num in lines:
        if move == "R":
            pwd += (n + num) // 100
            n = (n + num) % 100
        else:
            prev = n
            if n - num <= 0:
                pwd += ((num - n) // 100) + 1
                if prev == 0:
                    pwd -= 1  # Accommodate for case we are starting with 0
            n = (n - num) % 100

    return pwd


if __name__ == "__main__":
    day = 1
    dt = datetime(2025, 12, day)
    exp = {"a": 3, "b": 6}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
