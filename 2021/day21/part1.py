dice_state = 0


# https://adventofcode.com/2021/day/21
def solve(p1, p2):
  sc1, sc2 = 0, 0
  roll = 0

  turn = 1
  while sc1 < 1000 and sc2 < 1000:
    if turn == 1:
      p1, d = move(p1)
      sc1 += p1
      turn = 2
    else:
      p2, d = move(p2)
      sc2 += p2
      turn = 1
    roll += 3
    print(f"Player {1 if turn == 2 else 2} rolls {d} and moves to space {p1 if turn == 2 else p2} for a total score of {sc1 if turn == 2 else sc2}.")

  return min(sc1, sc2) * roll


def move(space):
  roll = roll_dice()
  s = sum(roll)
  next_space = 10 if (space+s) % 10 == 0 else (space+s) % 10
  return next_space, roll


def roll_dice():
  return (next_roll(), next_roll(), next_roll())


def next_roll():
  global dice_state
  dice_state = (dice_state + 1) if (dice_state + 1) <= 100 else (dice_state + 1) % 100
  return dice_state


if __name__ == '__main__':
  res = solve(2, 5)
  print(res)
