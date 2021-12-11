# https://adventofcode.com/2021/day/11
def solve(matrix, steps):
  if len(matrix) == 0:
    return 0

  n = len(matrix)
  m = len(matrix[0])

  count = 0
  for i in range(0, steps):
    flashed = [[False] * m for _ in range(0, n)]
    for j in range(0, n):
      for k in range(0, m):
        if not flashed[j][k]:
          matrix[j][k] += 1
          if matrix[j][k] > 9:
            count += flash_light((j, k), matrix, n, m, flashed)
    # [print(a) for a in flashed]
    # [print(a) for a in matrix]

  return count


def flash_light(coord, matrix, n, m, flashed):
  x, y = coord

  count = 1
  flashed[x][y] = True
  matrix[x][y] = 0  # reset to 0

  # Check surrounding positions
  for i in range(x-1, x+2):
    for j in range(y-1, y+2):
      if (i, j) != coord and i in range(0, n) and j in range(0, m) and not flashed[i][j]:
        matrix[i][j] += 1
        if matrix[i][j] > 9:
          count += flash_light((i, j), matrix, n, m, flashed)

  return count


def input_processing(content):
  return [[int(val.strip()) for val in line] for line in content.split('\n')[:-1]]


if __name__ == '__main__':
  f = open('input.txt')
  matrix = input_processing(f.read())
  print

  res = solve(matrix, 100)
  print(res)
