# https://adventofcode.com/2021/day/21
def solve(cuboids):
  N = 50
  N2 = N*2+1  # -50..50

  core = [[[0] * N2 for _ in range(N2)] for _ in range(N2)]

  for cb in cuboids:
    sig = cb[0]
    data = cb[1]
    values = [val for pair in data for val in pair]
    if min(values) < -N or max(values) > N:
      continue
    slots = [(i, j, k) for i in range(data[0][0], data[0][1]+1)
             for j in range(data[1][0], data[1][1]+1)
             for k in range(data[2][0], data[2][1]+1)]
    for slot in slots:
      x, y , z = slot
      core[x+N][y+N][z+N] = sig

  return sum([core[i][j][k] for i in range(N2) for j in range(N2) for k in range(N2)])


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
