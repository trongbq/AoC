from collections import defaultdict
import math


# https://adventofcode.com/2021/day/3
def solve(report):
  m = len(report)

  if m == 0:
    return 0

  # Find size of report binary value
  m = len(report)
  n = len(report[0])

  # Find rate of o2
  mem_o2 = [True] * m
  rem_o2 = m
  for i in range(0, n):
    count_one = 0
    for idx, val in enumerate(report):
      if mem_o2[idx] and val[i] == '1':
        count_one += 1

    target = '1' if count_one >= math.ceil(rem_o2 / 2.0) else '0'
    for idx, val in enumerate(report):
      if mem_o2[idx] and val[i] != target:
        mem_o2[idx] = False
        rem_o2 -= 1
    if rem_o2 == 1:
      break

  # Find rate of co2
  mem_co2 = [True] * m
  rem_co2 = m
  for i in range(0, n):
    count_one = 0
    # print("}}", val, i, idx, mem_o2[idx], val[i])
    for idx, val in enumerate(report):
      if mem_co2[idx] and val[i] == '1':
        count_one += 1

    target = '0' if count_one >= math.ceil(rem_co2 / 2.0) else '1'
    for idx, val in enumerate(report):
      if mem_co2[idx] and val[i] != target:
        mem_co2[idx] = False
        rem_co2 -= 1
    if rem_co2 == 1:
      break

  # Retrieve two rate numbers
  o2_rate = None
  co2_rate = None
  for i in range(0, m):
    if mem_o2[i]:
      o2_rate = report[i]
    if mem_co2[i]:
      co2_rate = report[i]

  # Convert to int and multiple to get final number
  return int(o2_rate, 2) * int(co2_rate, 2)



if __name__ == '__main__':
  f = open('input.txt')
  report = f.readlines()

  res = solve(report)
  print(res)
