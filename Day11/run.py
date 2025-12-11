from datetime import datetime

from utils import run_and_submit


def parse(filename: str):
    with open(filename, "r") as f:
        lines = f.read().strip().split("\n")

        G = {}
        for line in lines:
            src, dests = line.split(" ", 1)
            src = src[:-1]
            dests = dests.split(" ")
            G[src] = set(dests)

    return G


def find(G):
    S, E = "you", "out"
    PATHS = set()

    def dfs(curr, path):
        if curr == E:
            PATHS.add(tuple(path))
            return

        for neigh in G[curr]:
            path.append(neigh)
            dfs(neigh, path)
            path.pop()

    dfs(S, [S])
    return PATHS


def findp2(G):
    S, E = "svr", "out"

    # Graph does not contain cycles. Nodes cannot be revisited. Hence DP solution possible.
    cache = {}

    def dfs(curr, has_fft, has_dac):
        state = (curr, has_fft, has_dac)
        if curr == E:
            if has_fft and has_dac:
                return 1
            return 0

        if state in cache:
            return cache[state]

        total = 0
        for neigh in G[curr]:
            if neigh == "fft":
                total += dfs(neigh, True, has_dac)
            elif neigh == "dac":
                total += dfs(neigh, has_fft, True)
            else:
                total += dfs(neigh, has_fft, has_dac)

        cache[state] = total
        return total

    return dfs(S, False, False)


def run(filename: str):
    G = parse(filename)
    return len(find(G))


def runp2(filename: str):
    G = parse(filename)
    return findp2(G)


if __name__ == "__main__":
    day = 11
    dt = datetime(2025, 12, day)
    exp = {"a": 5, "b": 2}

    run_and_submit(f"Day{day}/sample.txt", "a", run, expected=exp["a"])
    run_and_submit(f"Day{day}/input.txt", "a", run, submit=True, dt=dt)
    run_and_submit(f"Day{day}/sample2.txt", "b", runp2, expected=exp["b"])
    run_and_submit(f"Day{day}/input.txt", "b", runp2, submit=True, dt=dt)
