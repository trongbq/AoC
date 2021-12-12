# https://adventofcode.com/2021/day/6
def solve(timers, days):
  if len(timers) == 0:
    return 0

  for day in range(0, days):
    for i in range(0, len(timers)):
      if timers[i] == 0:
        timers[i] = 6  # reset timers
        timers.append(8) # newborn lanternfish
      else:
        timers[i] -= 1
        
  return len(timers)


def input_processing(content):
  return [int(val.strip()) for val in content.split(',')]


if __name__ == '__main__':
  f = open('input.txt')
  timers = input_processing(f.read())
  days = 80

  res = solve(timers, days)
  print(res)
