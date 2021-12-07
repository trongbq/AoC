# https://adventofcode.com/2021/day/5
def solve(positions):
  if len(positions) == 0:
    return 0

  min_fuel = float('inf')
  min_position = -1

  # Try all possible position that might take least fuel
  # Range from smallest existing position to largest existing position
  for i in range(min(positions), max(positions) + 1):
    temp = 0
    for p in positions:
      temp += abs(p - i)  # calculate required fuel to take it to position i
    if temp < min_fuel:
      min_fuel = temp
      min_position = i

  return min_fuel, min_position


def input_processing(content):
  return [int(val.strip()) for val in content.split(',')]


if __name__ == '__main__':
  f = open('input.txt')
  positions = input_processing(f.read())
  days = 80

  res = solve(positions)
  print(res)
