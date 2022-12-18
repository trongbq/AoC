import sys
import re
from tqdm import tqdm


def parse_input(file_name):
    rates = {}
    connected = {}
    order = {}

    lines = open(file_name, "r").readlines()
    for line in lines:
        line = line.strip()
        match = re.search(
            r"Valve ([A-Z]{2}) has flow rate=([0-9]+); tunnels? leads? to valves? ([A-Z\, ]+)",
            line,
        )
        name = match[1]

        rates[name] = int(match[2])
        connected[name] = match[3].split(", ")

    return rates, connected


def shortest_paths(connected):
    # use Floyd-Warshall algorithm to find all shortest paths,
    # it helps reducing our execution time,
    # so we don't have to go to adjacent valves to get to the target valve, with minimum cost
    valves = connected.keys()

    dist = {v: {vv: float("inf") for vv in valves} for v in valves}

    for valve, conn in connected.items():
        dist[valve][valve] = 0
        for v in conn:
            dist[valve][v] = 1

    for k in valves:
        for i in valves:
            for j in valves:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist


def pressure_on_path(path, dist, rates, t):
    total = 0
    valve = "AA"
    for next_valve in path:
        t = t - dist[valve][next_valve] - 1
        total += rates[next_valve] * t
        valve = next_valve
    return total


def all_paths_from(valve, rates, dist, start):
    paths = []

    # find the path that could produce largest pressure
    # every valves in a certain path are opened and have positive flow rate
    def dfs(valve, t, pressure, visited):
        if t <= 0:
            return

        next_valves = [(v, d) for v, d in dist[valve].items() if rates[v] != 0 and v not in visited]

        for (v, d) in next_valves:
            dfs(v, t - d - 1, pressure + rates[v] * (t - d - 1), visited + [v])

        paths.append(visited)

    dfs(valve, start, 0, [])
    return paths


def solo(rates, dist):
    paths = all_paths_from("AA", rates, dist, 30)
    return max([pressure_on_path(path, dist, rates, 30) for path in paths])


def with_elephant(rates, dist):
    paths = all_paths_from("AA", rates, dist, 26)

    # pre-compute pressures on all paths
    pressures = []
    for p in paths:
        pressures.append(pressure_on_path(p, dist, rates, 26))

    mp = 0
    n = len(paths)
    with tqdm(total=n - 1) as pbar:
        for i in range(n - 1):
            for j in range(i + 1, n):
                if set(paths[i]).isdisjoint(paths[j]):
                    mp = max(mp, pressures[i] + pressures[j])
            pbar.update(1)
    return mp


def main(file_name):
    rates, connected = parse_input(file_name)
    print("Completed reading input")

    dist = shortest_paths(connected)
    print("Completed find all shortest paths")

    print("Part 1: ", solo(rates, dist))
    print("Part 2: ", with_elephant(rates, dist))


if __name__ == "__main__":
    file_name = "input_sample.txt" if len(sys.argv) > 1 and sys.argv[1] == "-t" else "input.txt"
    main(file_name)
