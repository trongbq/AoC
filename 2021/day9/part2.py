import functools


# https://adventofcode.com/2021/day/9
def solve(matrix):
  if len(matrix) == 0:
    return 0

  n = len(matrix)
  m = len(matrix[0])

  lowest_points = []
  for i in range(0, n):
    for j in range(0, m):
      valid = True
      val = matrix[i][j]
      if i > 0 and matrix[i-1][j] <= val:
        valid = False
      if j > 0 and matrix[i][j-1] <= val:
        valid = False
      if i < n-1 and matrix[i+1][j] <= val:
        valid = False
      if j < m-1 and matrix[i][j+1] <= val:
        valid = False
      if valid:
        lowest_points.append((i, j))

  basins = []
  for point in lowest_points:
    visited = [[False] * m for i in range(0, n)]
    c = find_basins(point, matrix, n, m, visited)
    basins.append(c)

  # Get three largest basins and multiply them together
  return functools.reduce(lambda a, b: a*b, sorted(basins)[-3:], 1)


def find_basins(coord, matrix, n, m, visited):
  x, y = coord

  # 9 is not in the basin
  if matrix[x][y] == 9:
    return 0

  if visited[x][y]:
    return 0

  count = 1
  # Mark this slot as visited
  visited[x][y] = True

  if x - 1 >= 0 and matrix[x-1][y] - matrix[x][y] >= 1:
    count += find_basins((x-1, y), matrix, n, m, visited)
  if y - 1 >= 0 and matrix[x][y-1] - matrix[x][y] >= 1:
    count += find_basins((x, y-1), matrix, n, m, visited)
  if x + 1 < n and matrix[x+1][y] - matrix[x][y] >= 1:
    count += find_basins((x+1, y), matrix, n, m, visited)
  if y + 1 < m and matrix[x][y+1] - matrix[x][y] >= 1:
    count += find_basins((x, y+1), matrix, n, m, visited)

  return count


def input_processing(content):
  return [[int(val.strip()) for val in line] for line in content.split('\n')[:-1]]


if __name__ == '__main__':
  f = open('input.txt')
  matrix = input_processing(f.read())

  res = solve(matrix)
  print(res)
