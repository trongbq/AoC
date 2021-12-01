# https://adventofcode.com/2021/day/1
# How many measurements are larger than the previous measurement?
def run_part1(values):
  count = 0
  prev = None
  for value in values:
    if prev != None:
      if value - prev > 0:
        count += 1
    prev = value
  return count

# https://adventofcode.com/2021/day/1#part2
# How many sums are larger than the previous sum?
def run_part2(values):
  if len(values) <= 3:
    return 0

  count = 0
  prev_sum = None
  # Use i as index to get slice of 3 values in the list
  for i in range(0, len(values)-2):
    sub_sum = sum(values[i:i+3])

    if prev_sum != None:
      if sub_sum > prev_sum:
        count += 1
    prev_sum = sub_sum

  return count

if __name__ == '__main__':
  f = open('input/day1.txt')
  values = [int(val) for val in f.readlines()]

  res = run_part2(values)
  print(res)
