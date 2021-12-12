# https://adventofcode.com/2021/day/6
def solve(timers, days):
  if len(timers) == 0:
    return 0

  # fish have same internal timers share same behaviors
  # group them together
  n = 9  # maximum 9 slots from 0 to 8
  bucket = [0] * n
  for val in timers:
    bucket[val] += 1

  for day in range(0, days):
    temp = bucket[0]  # number of fishes about to create new fishes
    # countdown for fish from slot 1 to 8 by moving them down to below slot
    for i in range(0, n-1):
      bucket[i] = bucket[i+1]
    bucket[8] = 0
    # fishes which was in slot 0 now produce two output: reset and newborn
    bucket[6] += temp
    bucket[8] += temp

  return sum(bucket)


def input_processing(content):
  return [int(val.strip()) for val in content.split(',')]


if __name__ == '__main__':
  f = open('input.txt')
  timers = input_processing(f.read())
  days = 256

  res = solve(timers, days)
  print(res)
