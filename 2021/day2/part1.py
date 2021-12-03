# https://adventofcode.com/2021/day/2
# What do you get if you multiply your final horizontal position by your final depth?
def solve(commands):
  horizontal_pos = 0
  depth_pos = 0

  for command in commands:
    c, unit = command.split()
    unit = int(unit)

    if c == 'forward':
      horizontal_pos += unit
    elif c == 'up':
      depth_pos -= unit
    elif c == 'down':
      depth_pos += unit
    else:
      print("Invalid command")
      # Skip it

  return horizontal_pos * depth_pos


if __name__ == '__main__':
  f = open('input.txt')
  planned_course = f.readlines()

  res = solve(planned_course)
  print(res)
