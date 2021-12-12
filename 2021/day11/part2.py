# https://adventofcode.com/2021/day/11
def solve(matrix):
  if len(matrix) == 0:
    return 0

  n = len(matrix)
  m = len(matrix[0])

  steps = 0
  while True:
    steps += 1
    flashed = [[False] * m for _ in range(0, n)]
    for j in range(0, n):
      for k in range(0, m):
        if not flashed[j][k]:
          matrix[j][k] += 1
          if matrix[j][k] > 9:
            flash_light((j, k), matrix, n, m, flashed)

    # Check if all flashed in this step
    if all([flashed[x][y] for x in range(0, n) for y in range(0, m)]):
      return steps


def flash_light(coord, matrix, n, m, flashed):
  x, y = coord

  flashed[x][y] = True
  matrix[x][y] = 0  # reset to 0

  # Check surrounding positions
  for i in range(x-1, x+2):
    for j in range(y-1, y+2):
      if (i, j) != coord and i in range(0, n) and j in range(0, m) and not flashed[i][j]:
        matrix[i][j] += 1
        if matrix[i][j] > 9:
          flash_light((i, j), matrix, n, m, flashed)


def input_processing(content):
  return [[int(val.strip()) for val in line] for line in content.split('\n')[:-1]]


if __name__ == '__main__':
  f = open('input.txt')
  matrix = input_processing(f.read())
  print

  res = solve(matrix)
  print(res)
