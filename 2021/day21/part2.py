from functools import cache
import itertools


outcome = [sum(rolls) for rolls in itertools.product([1, 2, 3], repeat=3)]

# https://adventofcode.com/2021/day/21
def solve(p1, p2):
  return take_turn(0, 0, p1, p2, 1)


@cache
def take_turn(sc1, sc2, p1, p2, turn):
  if sc1 >= 21:
    return 1, 0
  if sc2 >= 21:
    return 0, 1
  
  spaces = [move(p1 if turn == 1 else p2, rolls) for rolls in outcome]
  if turn == 1:
    result = [take_turn(sc1+s, sc2, s, p2, 2) for s in spaces]
  else:
    result = [take_turn(sc1, sc2+s, p1, s, 1) for s in spaces]

  temp = (sum([a for a, _ in result]), sum([b for _, b in result]))
  return temp


def move(space, s):
  next_space = 10 if (space+s) % 10 == 0 else (space+s) % 10
  return next_space


if __name__ == '__main__':
  res = solve(2, 5)
  print(res)
