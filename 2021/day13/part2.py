from collections import defaultdict


# https://adventofcode.com/2021/day/13
def solve(coords, folds):
  if len(coords) == 0:
    return 0

  # x horizontal, y vertical
  x_max = max([coord[0] for coord in coords])
  y_max = max([coord[1] for coord in coords])

  matrix = [['.'] * (x_max+1) for _ in range(0, y_max+1)]

  # Mark all existing point in this matrix
  for coord in coords:
    matrix[coord[1]][coord[0]] = '#'

  # Start folding
  for fold in folds:
    fold_line = fold[1]
    if fold[0] == 'x':
      # Fold vertically
      for i in range(0, len(matrix)):
        for j in range(fold_line-1, -1, -1):
          matrix[i][j] = '#' if matrix[i][j] == '#' or matrix[i][fold_line + fold_line - j] == '#' else '.'
      matrix = [row[:fold_line] for row in matrix]
    else:
      # Fold horizontally
      for i in range(fold_line-1, -1, -1):
        for j in range(0, len(matrix[0])):
          matrix[i][j] = '#' if matrix[i][j] == '#' or matrix[fold_line + fold_line - i][j] == '#' else '.'
      matrix = matrix[:fold_line]

  [print(' '.join(row)) for row in matrix]

  return sum([row.count('#') for row in matrix])


# Use map list to present graph data
def input_processing(content):
  section1, section2 = content.split('\n\n')

  coords = []
  for line in section1.strip().split('\n'):
    a, b = line.strip().split(',')
    coords.append([int(a), int(b)])

  folds = []
  for line in section2.strip().split('\n'):
    a, b = line.strip()[11:].split('=')
    folds.append([a, int(b)]) 

  return coords, folds


if __name__ == '__main__':
  f = open('input.txt')
  coords, folds = input_processing(f.read())

  res = solve(coords, folds)
  print(res)
