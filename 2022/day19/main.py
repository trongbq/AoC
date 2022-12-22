import sys
import json
import re
from enum import Enum
from copy import deepcopy

INPUT_PATTERN = "Blueprint (?P<id>\d+): Each ore robot costs (?P<ore>\d+) ore. Each clay robot costs (?P<clay_ore>\d+) ore. Each obsidian robot costs (?P<obsidian_ore>\d+) ore and (?P<obsidian_clay>\d+) clay. Each geode robot costs (?P<geode_ore>\d+) ore and (?P<geode_obsidian>\d+) obsidian."

Choice = Enum("Choice", ["BUILD_ORE_ROBOT", "BUILD_CLAY_ROBOT", "BUILD_OBSIDIAN_ROBOT", "BUILD_GEODE_ROBOT", "NONE"])


class Resource:
    def __init__(self, ore, clay, obsidian, geode):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def subtract(self, other):
        self.ore = self.ore - other.ore
        self.clay = self.clay - other.clay
        self.obsidian = self.obsidian - other.obsidian
        self.geode = self.geode - other.geode


class Blueprint:
    def __init__(self, ore_robot, clay_robot, obsidian_robot, geode_robot):
        self.ore_robot_cost = ore_robot
        self.clay_robot_cost = clay_robot
        self.obsidian_robot_cost = obsidian_robot
        self.geode_robot_cost = geode_robot
        self.max_ore_needed = max([ore_robot.ore, clay_robot.ore, obsidian_robot.ore, geode_robot.ore])
        self.max_clay_needed = obsidian_robot.clay
        self.max_obsidian_needed = geode_robot.obsidian

    def __repr__(self):
        return f"Each ore robot costs {self.ore_robot_cost.ore} ore. Each clay robot costs {self.clay_robot_cost.ore} ore. Each obsidian robot costs {self.obsidian_robot_cost.ore} ore and {self.obsidian_robot_cost.clay} clay. Each geode robot costs {self.geode_robot_cost.ore} ore and {self.geode_robot_cost.obsidian} obsidian."

    @staticmethod
    def parse_input(line):
        match = re.search(INPUT_PATTERN, line)

        ore_robot = Resource(int(match.group("ore")), 0, 0, 0)
        clay_robot = Resource(int(match.group("clay_ore")), 0, 0, 0)
        obsidian_robot = Resource(int(match.group("obsidian_ore")), int(match.group("obsidian_clay")), 0, 0)
        geode_robot = Resource(int(match.group("geode_ore")), 0, int(match.group("geode_obsidian")), 0)

        return Blueprint(ore_robot, clay_robot, obsidian_robot, geode_robot)


class State:
    def __init__(self):
        self.resource = Resource(0, 0, 0, 0)
        self.ore_robot = 1
        self.clay_robot = 0
        self.obsidian_robot = 0
        self.geode_robot = 0

    def update(self, blueprint, choice):
        updated_state = deepcopy(self)
        if choice == Choice.BUILD_ORE_ROBOT:
            updated_state.resource.subtract(blueprint.ore_robot_cost)
            updated_state.ore_robot += 1
        elif choice == Choice.BUILD_CLAY_ROBOT:
            updated_state.resource.subtract(blueprint.clay_robot_cost)
            updated_state.clay_robot += 1
        elif choice == Choice.BUILD_OBSIDIAN_ROBOT:
            updated_state.resource.subtract(blueprint.obsidian_robot_cost)
            updated_state.obsidian_robot += 1
        elif choice == Choice.BUILD_GEODE_ROBOT:
            updated_state.resource.subtract(blueprint.geode_robot_cost)
            updated_state.geode_robot += 1

        updated_state.resource.ore += self.ore_robot
        updated_state.resource.clay += self.clay_robot
        updated_state.resource.obsidian += self.obsidian_robot
        updated_state.resource.geode += self.geode_robot

        return updated_state

    def can_build_robot(self, blueprint, choice):
        if choice == Choice.BUILD_ORE_ROBOT:
            return self.resource.ore >= blueprint.ore_robot_cost.ore
        elif choice == Choice.BUILD_CLAY_ROBOT:
            return self.resource.ore >= blueprint.clay_robot_cost.ore
        elif choice == Choice.BUILD_OBSIDIAN_ROBOT:
            return (
                self.resource.ore >= blueprint.obsidian_robot_cost.ore
                and self.resource.clay >= blueprint.obsidian_robot_cost.clay
            )
        elif choice == Choice.BUILD_GEODE_ROBOT:
            return (
                self.resource.ore >= blueprint.geode_robot_cost.ore
                and self.resource.obsidian >= blueprint.geode_robot_cost.obsidian
            )
        return False

    def to_key(self):
        return (
            self.resource.ore,
            self.resource.clay,
            self.resource.obsidian,
            self.ore_robot,
            self.clay_robot,
            self.obsidian_robot,
        )

    def __repr__(self):
        return f"Resources: ore:{self.resource.ore}, clay:{self.resource.clay}, obisidian:{self.resource.obsidian}, geode:{self.resource.geode}, Robots: ore:{self.ore_robot}, clay:{self.clay_robot}, obisidian:{self.obsidian_robot}, geode:{self.geode_robot}"


def parse_input(file_name):
    lines = open(file_name, "r").readlines()
    blueprints = []
    for line in lines:
        blueprints.append(Blueprint.parse_input(line.strip()))
    return blueprints


def maxmium_geode(blueprint, duration):
    mem = {}
    max_geode_robot_in_time = [(i - 1) * i // 2 for i in range(duration + 1)]
    max_geode_sofar = 0

    def collect_and_build(t, state, geode):
        nonlocal max_geode_sofar

        if t <= 1:
            max_geode_sofar = max(max_geode_sofar, geode)
            return 0

        mem_key = (t, state.to_key())
        if mem_key in mem:
            max_geode_sofar = max(max_geode_sofar, geode + mem[mem_key])
            # return the best number of geode we can collect given number of remaining time,
            # (ore, clay, obsidian), (ore robots, clay robots, obsidian robots)
            return mem[mem_key]

        possible_max_geode = state.resource.geode + (state.geode_robot * t) + max_geode_robot_in_time[t]
        if possible_max_geode <= max_geode_sofar:
            return float("-inf")

        max_geode = 0

        if state.can_build_robot(blueprint, Choice.BUILD_ORE_ROBOT):
            updated_state = state.update(blueprint, Choice.BUILD_ORE_ROBOT)
            max_geode = max(max_geode, collect_and_build(t - 1, updated_state, geode))

        if state.can_build_robot(blueprint, Choice.BUILD_CLAY_ROBOT):
            updated_state = state.update(blueprint, Choice.BUILD_CLAY_ROBOT)
            max_geode = max(max_geode, collect_and_build(t - 1, updated_state, geode))

        if state.can_build_robot(blueprint, Choice.BUILD_OBSIDIAN_ROBOT):
            updated_state = state.update(blueprint, Choice.BUILD_OBSIDIAN_ROBOT)
            max_geode = max(max_geode, collect_and_build(t - 1, updated_state, geode))

        if state.can_build_robot(blueprint, Choice.BUILD_GEODE_ROBOT):
            updated_state = state.update(blueprint, Choice.BUILD_GEODE_ROBOT)
            max_geode = max(max_geode, collect_and_build(t - 1, updated_state, geode + (t - 1)) + (t - 1))

        updated_state = state.update(blueprint, Choice.NONE)
        max_geode = max(max_geode, collect_and_build(t - 1, updated_state, geode))

        mem[mem_key] = max_geode

        return max_geode

    return collect_and_build(duration, State(), 0)


def total_quality_level(blueprints):
    total = 0
    for i, bp in enumerate(blueprints):
        geode = maxmium_geode(bp, 24)
        print(i, geode)
        total += (i + 1) * geode
    return total


def first_three_blueprints(blueprints):
    total = 1
    for i, bp in enumerate(blueprints[:3]):
        geode = maxmium_geode(bp, 32)
        print(i, geode)
        total *= geode
    return total


def main(file_name):
    blueprints = parse_input(file_name)

    print("Part 1:", total_quality_level(blueprints))
    print("Part 2:", first_three_blueprints(blueprints))


if __name__ == "__main__":
    file_name = "input_sample.txt" if len(sys.argv) > 1 and sys.argv[1] == "-t" else "input.txt"
    main(file_name)
