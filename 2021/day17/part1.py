# https://adventofcode.com/2021/day/17
def solve(target):
  (x1, x2), (y1, y2) = target

  coord = (None, None)
  max_y = float('-inf')
  for i in range(1, 1000):  # wew, try bruteforce
    for j in range(1, x2+1):
      hit, temp_max_y = check(j, i, target)
      if hit:
        if temp_max_y > max_y:
          max_y = temp_max_y
          coord = (j, i)
  
  return coord, max_y


def check(a, b, target):
  (x1, x2), (y1, y2) = target

  x, y = 0, 0
  vx, vy = a, b
  max_y = float('-inf')
  while True:
    # Update current position
    x = x + vx
    y = y + vy

    # Keep eyes on maximum value of y
    if y > max_y:
      max_y = y

    # Update velocity change after this step
    vx = vx - 1 if vx > 0 else 0 if vx == 0 else vx + 1
    vy = vy - 1

    if x >= x1 and x <= x2 and y >= y1 and y <= y2:
      return True, max_y

    if x > x2 or y < y2:
      return False, -1


def input_processing(content):
  content = content[len('target area: '):]
  x_coords, y_coords = content.split(',')
  x1, x2 = x_coords.strip()[len('x='):].split('..')
  y1, y2 = y_coords.strip()[len('y='):].split('..')
  
  return ((int(x1), int(x2)), (int(y1), int(y2)))


if __name__ == '__main__':
  f = open('input.txt')
  target = input_processing(f.read())
  print(target)

  res = solve(target)
  print(res)
