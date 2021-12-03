from collections import defaultdict


# https://adventofcode.com/2021/day/3
def solve(report):
  m = len(report)

  if m == 0:
    return 0

  # Find size of report binary value
  m = len(report)
  n = len(report[0])

  # Collect insights on report for 1's
  count_one = defaultdict(lambda: 0)
  for val in report:
    for i in range(0, n):
      if val[i] == '1':
        count_one[i] += 1
  
  # Get binary value from insight we got
  gamma_rate = ''
  esp_rate = ''
  for k, v in sorted(count_one.items()):
    if v > m // 2:
      gamma_rate += '1'
      esp_rate += '0'
    else:
      gamma_rate += '0'
      esp_rate += '1'
  
  # Convert to int and multiple to get final number
  return int(gamma_rate, 2) * int(esp_rate, 2)



if __name__ == '__main__':
  f = open('input.txt')
  report = f.readlines()

  res = solve(report)
  print(res)
