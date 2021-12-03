# https://adventofcode.com/2021/day/1
# How many measurements are larger than the previous measurement?
def solve(values):
  count = 0
  prev = None
  for value in values:
    if prev != None:
      if value - prev > 0:
        count += 1
    prev = value
  return count


if __name__ == '__main__':
  f = open('input.txt')
  values = [int(val) for val in f.readlines()]

  res = solve(values)
  print(res)
