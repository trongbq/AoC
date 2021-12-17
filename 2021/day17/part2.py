# https://adventofcode.com/2021/day/17#part2
def solve(target):
  (x1, x2), (y1, y2) = target

  count = 0
  for i in range(-1000, 1000):  # wew, try bruteforce
    for j in range(1, x2+1):
      hit = check(j, i, target)
      if hit:
        count += 1
  
  return count


def check(a, b, target):
  (x1, x2), (y1, y2) = target

  x, y = 0, 0
  vx, vy = a, b
  while True:
    # Update current position
    x = x + vx
    y = y + vy

    # Update velocity change after this step
    vx = vx - 1 if vx > 0 else 0 if vx == 0 else vx + 1
    vy = vy - 1

    if x >= x1 and x <= x2 and y >= y1 and y <= y2:
      return True

    if x > x2 or y < y1:
      return False


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
