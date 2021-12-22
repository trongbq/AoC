import copy


# https://adventofcode.com/2021/day/21
def solve(cuboids):
  core = []  # holds all blocks which have all cure turn on
  core.append(cuboids[0][1])

  for sig, data in cuboids[1:]:
    curr_core = copy.deepcopy(core)
    core = []
    for i in range(len(curr_core)):
      yes = intersect(curr_core[i], data)
      if yes:
        core += difference(curr_core[i], data)
      else:
        core.append(curr_core[i])
    if sig == 1:
      # Current block is turn on, so add it to the core
      core.append(data)

  return sum([
    (abs(cb[0][0]-cb[0][1])+1) * 
    (abs(cb[1][0]-cb[1][1])+1) *
    (abs(cb[2][0]-cb[2][1])+1) for cb in core])


# Remove b from a
def difference(a, b):
  # Split each axis in `a` into at most 3 parts: low, common/intersect, high
  x_lines = different_lines(a[0], b[0]) + [intersect_line(a[0], b[0])]
  y_lines = different_lines(a[1], b[1]) + [intersect_line(a[1], b[1])]
  z_lines = different_lines(a[2], b[2]) + [intersect_line(a[2], b[2])]

  # Split block `a` into multiple smaller block based on position of block `b`
  blocks = []
  for i in range(len(x_lines)):
    for j in range(len(y_lines)):
      for k in range(len(z_lines)):
        if i == (len(x_lines)-1) and j == (len(y_lines)-1) and k == (len(z_lines)-1):
          # This is common/intersect block -> skip
          continue
        if not x_lines[i] or not y_lines[j] or not z_lines[k]:
          # Invalid block (go out of range of block `a` so some axis value is 0) -> skip
          continue
        blocks.append((x_lines[i], y_lines[j], z_lines[k]))
  return blocks


# Collect lines in a that is splited by b, which in the same axis
def different_lines(a, b):
  lines = []
  if a[0] < b[0]:
    lines.append((a[0], b[0]-1))
  if a[1] > b[1]:
    lines.append((b[1]+1, a[1]))
  return lines


def intersect_line(a, b):
  return max(a[0], b[0]), min(a[1], b[1])


def intersect(a, b):
  return line_intersect(a[0], b[0]) and line_intersect(a[1], b[1]) and line_intersect(a[2], b[2])


# a.s < b.e and b.s < a.e
def line_intersect(a, b):
  return a[0] <= b[1] and b[0] <= a[1]


def input_processing(content):
  cb_lines = content.strip().split('\n')
  cuboids = []
  for line in cb_lines:
    if line.find('on ') != -1:
      line = line.strip()[3:]  # strip `on` prefix
      signal = 1
    else:
      line = line.strip()[4:]  # strip `off` prefix
      signal = 0
    cuboids.append(
      (
        signal,
        tuple(
          tuple([int(it) for it in val.strip()[2:].split('..')])  # strip prefix and split
          for val in line.split(',')
        )
      )
    )
    
  lo, hi  = float('inf'), float('-inf')
  for cb in cuboids:
    vs = [val for pair in cb[1] for val in pair]
    lo, hi = min(lo, min(vs)), max(hi, max(vs))
  print("Min:", lo, "max:", hi)

  return cuboids


if __name__ == '__main__':
  f = open('input.txt')
  cuboids = input_processing(f.read())

  res = solve(cuboids)
  print(res)
