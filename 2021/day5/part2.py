# https://adventofcode.com/2021/day/5
def solve(coords):
  if len(coords) == 0:
    return 0

  # Find maximum value of x and y to form diagram
  max_x = -1
  max_y = -1
  for coord in coords:
    if coord[0][0] > max_x:
      max_x = coord[0][0]
    if coord[1][0] > max_x:
      max_x = coord[1][0]
    if coord[1][0] > max_y:
      max_y = coord[1][0]
    if coord[1][1] > max_y:
      max_y = coord[1][1]
    
  # Plus 1 for 0
  diagram = [[0] * (max_y+1) for i in range(0, max_x+1)]

  # Go through all valid coordinates and mark on diagram
  for coord in coords:
    if coord[0][0] == coord[1][0]:
      # Go horizontal line
      low, high = (coord[0][1], coord[1][1]) if coord[0][1] <= coord[1][1] else (coord[1][1], coord[0][1])
      for i in range(low, high+1):
        diagram[coord[0][0]][i] += 1
    elif coord[0][1] == coord[1][1]:
      # Go vertical line
      low, high = (coord[0][0], coord[1][0]) if coord[0][0] <= coord[1][0] else (
          coord[1][0], coord[0][0])
      for i in range(low, high+1):
        diagram[i][coord[0][1]] += 1
    else:
      # Go diagonal line
      if coord[0][0] < coord[1][0]:
        if coord[0][1] < coord[1][1]:
          # I section
          for i in range(0, coord[1][0] - coord[0][0] + 1):
              diagram[coord[0][0] + i][coord[0][1] + i] += 1
        else:
          # II section
          for i in range(0, coord[1][0] - coord[0][0] + 1):
              diagram[coord[0][0] + i][coord[0][1] - i] += 1
      else:
        if coord[0][1] < coord[1][1]:
          # III section
          for i in range(0, coord[0][0] - coord[1][0] + 1):
              diagram[coord[1][0] + i][coord[1][1] - i] += 1
        else:
          # IV section
          for i in range(0, coord[0][0] - coord[1][0] + 1):
              diagram[coord[1][0] + i][coord[1][1] + i] += 1

  count = 0
  for i in range(0, max_x+1):
    for j in range(0, max_y+1):
      if diagram[i][j] >= 2:
        count += 1

  return count


def input_processing(lines):
  coords = []
  for line in lines:
    coord = [[int(val) for val in part.strip().split(',')] for part in line.split('->')]
    # Only consider horizontal, vertical lines or 45 degree diagonal
    if coord[0][0] == coord[1][0] or coord[0][1] == coord[1][1] or abs(coord[0][0] - coord[1][0]) == abs(coord[0][1] - coord[1][1]):
      coords.append(coord)
  return coords


if __name__ == '__main__':
  f = open('input.txt')
  coords = input_processing(f.readlines())

  res = solve(coords)
  print(res)
