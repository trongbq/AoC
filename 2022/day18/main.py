import sys
import queue

ADJACENT = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]


def parse_input(file_name):
    lines = open(file_name, "r").readlines()
    return [tuple(map(lambda x: int(x), line.strip().split(","))) for line in lines]


def are_connected_cubes(c1, c2):
    # use Manhattan distance to check for connected
    return sum([abs(c1[i] - c2[i]) for i in range(3)]) == 1


def surface_area(cubes):
    covered_sides = 0
    n = len(cubes)

    # take single cube and check with remaining cubes to see if they are connected
    # if they are, we got two cubes facing each other, losing 2 sides covered
    for i in range(n):
        for j in range(i + 1, n):
            if are_connected_cubes(cubes[i], cubes[j]):
                covered_sides += 2

    return 6 * n - covered_sides


def adjacent_cubes(cube, min_coord, max_coord):
    adj_cubes = [(cube[0] + adj[0], cube[1] + adj[1], cube[2] + adj[2]) for adj in ADJACENT]
    # filter only cubes in valid area
    return filter(
        lambda x: all([x[i] >= min_coord[i] for i in range(3)]) and all([x[i] <= max_coord[i] for i in range(3)]),
        adj_cubes,
    )


def exterior_surface_area(cubes):
    # get imagine big cube surrounding the lava drolet
    min_coord = [float("inf"), float("inf"), float("inf")]
    max_coord = [float("-inf"), float("-inf"), float("-inf")]

    for cube in cubes:
        min_coord[0] = min(min_coord[0], cube[0])
        min_coord[1] = min(min_coord[1], cube[1])
        min_coord[2] = min(min_coord[2], cube[2])
        max_coord[0] = max(max_coord[0], cube[0])
        max_coord[1] = max(max_coord[1], cube[1])
        max_coord[2] = max(max_coord[2], cube[2])

    # add 1 extra room for water to flow, simulate surrounding area
    min_coord = tuple([val - 1 for val in min_coord])
    max_coord = tuple([val + 1 for val in max_coord])

    # flood fill in 3D, with key is cube coordinate, value is boolean (True means filled with water, False means lava cube and can not move further)
    # coordinates that not in this data are considered to be cubes of air since water can not reach them.
    flood_filled = {}

    q = queue.Queue()
    q.put(min_coord)  # start from lowest point

    while not q.empty():
        cube = q.get()
        if cube not in cubes:
            flood_filled[cube] = True
            # try to reach adjacent cubes in 6 directions
            for adj_cube in adjacent_cubes(cube, min_coord, max_coord):
                if adj_cube not in flood_filled:
                    # keep track of cube in the data to avoid duplicate cube in the queue
                    flood_filled[adj_cube] = False
                    q.put(adj_cube)

    # count number of air cube
    air_cubes = []
    for x in range(min_coord[0], max_coord[0] + 1):
        for y in range(min_coord[1], max_coord[1] + 1):
            for z in range(min_coord[2], max_coord[2] + 1):
                if (x, y, z) not in flood_filled and (x, y, z) not in cubes:
                    air_cubes.append((x, y, z))

    # air cubes might be connected so should get surface area of these air cubes
    # instead of assume always 6 sides of air cubes touch lava cubes
    return surface_area(cubes) - surface_area(air_cubes)


def main(file_name):
    cubes = parse_input(file_name)

    print("Part 1:", surface_area(cubes))
    print("Part 2:", exterior_surface_area(cubes))


if __name__ == "__main__":
    file_name = "input_sample.txt" if len(sys.argv) > 1 and sys.argv[1] == "-t" else "input.txt"
    main(file_name)
