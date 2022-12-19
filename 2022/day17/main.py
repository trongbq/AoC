import sys

WIDTH_CHAMBER = 7
START_DISTANCE = 3


def parse_input(file_name):
    return open(file_name, "r").readline().strip()


def get_next_rock(i):
    rocks = [
        [[1, 1, 1, 1]],
        [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
        [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
        [[1], [1], [1], [1]],
        [[1, 1], [1, 1]],
    ]
    return rocks[(i - 1) % 5]


def move_rock(chamber, rock, offset):
    for row in range(0, len(rock)):
        for col in range(0, len(rock[row])):
            if rock[row][col] == 1:
                chamber[row + offset[0]][col + offset[1]] = rock[row][col]


def check_rock_collision_jet(chamber, rock, next_offset):
    for row in range(0, len(rock)):
        for col in range(0, len(rock[row])):
            if (row + next_offset[1]) < 0 or (col + next_offset[1]) >= WIDTH_CHAMBER:
                return True
            if rock[row][col] == 1 and chamber[row + next_offset[0]][col + next_offset[1]] == 1:
                return True
    return False


def check_rock_collision_down(chamber, rock, next_offset):
    for row in range(0, len(rock)):
        for col in range(0, len(rock[row])):
            if (row + next_offset[0]) >= len(chamber):
                return True
            if rock[row][col] == 1 and chamber[row + next_offset[0]][col + next_offset[1]] == 1:
                return True
    return False


def trim_chamber(chamber):
    for i in range(len(chamber)):
        if any(chamber[i]):
            return chamber[i:]


def visual_chamber(chamber):
    for r in range(len(chamber)):
        for c in range(len(chamber[r])):
            print("." if chamber[r][c] == 0 else "#", end=" ")
        print()


def cover_the_floor(chamber):
    # only check latest two rows
    if len(chamber) < 2:
        return False

    s = [chamber[0][i] + chamber[1][i] for i in range(WIDTH_CHAMBER)]
    return all([it > 0 for it in s])


def part1():
    jet = parse_input(file_name)

    chamber = []

    curr_jet = -1
    rock_number = 1

    target_rock = 2022

    while True:
        rock = get_next_rock(rock_number)
        offset = [0, 2]
        chamber = [[0] * WIDTH_CHAMBER for _ in range(len(rock) + START_DISTANCE)] + chamber

        # check current jet and fall down 1 unit until it stops
        while True:
            # horizontally
            curr_jet = (curr_jet + 1) % len(jet)

            if jet[curr_jet] == "<":
                next_offset = [offset[0], offset[1] - 1]
            else:
                next_offset = [offset[0], offset[1] + 1]

            if not check_rock_collision_jet(chamber, rock, next_offset):
                offset = next_offset

            # down
            next_offset = [offset[0] + 1, offset[1]]
            if not check_rock_collision_down(chamber, rock, next_offset):
                offset = next_offset
            else:
                # collide, must stop and start new rock
                move_rock(chamber, rock, offset)
                break

        chamber = trim_chamber(chamber)

        if rock_number == target_rock:
            return len(chamber)

        rock_number += 1

    return -1


def part2():
    jet = parse_input(file_name)

    chamber = []

    curr_jet = -1
    rock_number = 1

    target_rock = 1000000000000
    cache = {}
    height = 0
    found_cycle = False

    while True:
        rock = get_next_rock(rock_number)
        offset = [0, 2]
        chamber = [[0] * WIDTH_CHAMBER for _ in range(len(rock) + START_DISTANCE)] + chamber

        # check current jet and fall down 1 unit until it stops
        while True:
            # horizontally
            curr_jet = (curr_jet + 1) % len(jet)

            if jet[curr_jet] == "<":
                next_offset = [offset[0], offset[1] - 1]
            else:
                next_offset = [offset[0], offset[1] + 1]

            if not check_rock_collision_jet(chamber, rock, next_offset):
                offset = next_offset

            # down
            next_offset = [offset[0] + 1, offset[1]]
            if not check_rock_collision_down(chamber, rock, next_offset):
                offset = next_offset
            else:
                # collide, must stop and start new rock
                move_rock(chamber, rock, offset)
                break

        chamber = trim_chamber(chamber)

        if not found_cycle and len(chamber) >= 2:
            area_key = int("".join([str(i) for i in chamber[0]]) + "".join([str(i) for i in chamber[1]]))
            if cover_the_floor(chamber):
                if (area_key, rock_number % 5, curr_jet) in cache:
                    # do some math to fast-forward til near the end
                    cached_rock_number, cached_chamber_height = cache[area_key, rock_number % 5, curr_jet]
                    cycle_rock_size = rock_number - cached_rock_number
                    if (target_rock - rock_number) > cycle_rock_size:
                        number_of_cycles = (target_rock - rock_number) // cycle_rock_size
                        cycle_height = len(chamber) - cached_chamber_height

                        rock_number += number_of_cycles * cycle_rock_size
                        height = cached_chamber_height + cycle_height * (number_of_cycles + 1)

                        # trim down chamber to contains only two lastest rows which cover full floor
                        chamber = chamber[:2]
                        height -= 2

                        found_cycle = True  # use this to avoid trying to detect multiple cycles, which not needed
                else:
                    cache[area_key, rock_number % 5, curr_jet] = (rock_number, len(chamber))

        if rock_number == target_rock:
            return height + len(chamber)

        rock_number += 1

    return -1


def main(file_name):
    print("Part 1:", part1())
    print("Part 2:", part2())


if __name__ == "__main__":
    file_name = "input_sample.txt" if len(sys.argv) > 1 and sys.argv[1] == "-t" else "input.txt"
    main(file_name)
