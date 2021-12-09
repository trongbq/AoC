# https://adventofcode.com/2021/day/5
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
        lowest_points.append(val)
  print(lowest_points)
  return sum([val + 1 for val in lowest_points])


def input_processing(content):
  return [[int(val.strip()) for val in line] for line in content.split('\n')[:-1]]


if __name__ == '__main__':
  f = open('input.txt')
  matrix = input_processing(f.read())

  res = solve(matrix)
  print(res)
