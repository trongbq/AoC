# https://adventofcode.com/2021/day/19#part2
def solve(scanners):
  N = len(scanners)
  origin = scanners[0]
  count = 1
  visited = [False for _ in range(N)]
  sc_origins = [(0, 0, 0)]
  while count < N:
    for i in range(1, N):
      if visited[i]:
        continue
      # check if overlap 12 coords
      print("checking overlap for scanner", i)
      overlap, correct, found_origin = check_overlapping(origin, scanners[i])
      if overlap:
        # add all coords to origin
        origin = merge_scanner(origin, correct)
        count += 1
        visited[i] = True
        sc_origins.append(found_origin)

  max_dist = float('-inf')
  for i in range(N-1):
    for j in range(i+1, N):
      dist = manhattan_dist(sc_origins[i], sc_origins[j])
      if dist > max_dist:
        max_dist = dist
  return max_dist


# Check is done by:
# 1. Create 24 variants which is the rotations of sb scanner
# 2. Check if sa scanner overlap with any of the variants
# Two scanner is overlap if existing a and b that have at least 12 common coordinates,
# where a and b are new scanner values of sa and sb
# which are updated by taking a coord in each scanner as origin and update remaining beacons to this new origin.
def check_overlapping(sa, sb):
  rotations = [[] for _ in range(24)]
  for j in range(len(sb)):
    ro = rotate(sb[j])
    for k in range(24):
      rotations[k].append(ro[k])

  for i in range(len(sa)):
    sa_new = swap_origin(i, sa)
    # for 24 variants, is any variants have 12 overlapping coords with sa_new
    for j in range(24):
      # check overlap for this j index variant
      variant = rotations[j]
      for k in range(len(sb)):
        sb_new = swap_origin(k, variant)
        # check this sb_new to sa_new to see if there are shared 12 coords
        # if there are, it means that sa[i] and variant[k] refer to the same beacon
        overlap = list(set(sa_new).intersection(set(sb_new)))
        if len(overlap) >= 12:
          # idxs = [(sb_new.index(it), sa_new.index(it)) for it in overlap]
          # for kk in idxs:
          #   print(sb[kk[0]], variant[kk[0]], sa[kk[1]])
          idx = sa_new.index(overlap[0])
          # select on overlap coord and get two coords in both scanner acoordingly to find out origin of sb scanner
          sb_origin = subtract(
              sa[sa_new.index(overlap[0])], variant[sb_new.index(overlap[0])])
          sb_right = convert_origin(sb_origin, variant)
          return True, sb_right, sb_origin
  return False, None, None


def merge_scanner(sa, sb):
  return list(set(sa + sb))


def convert_origin(o, scanner):
  new_sc = []
  for j in range(len(scanner)):
    new_sc.append(add(scanner[j], o))
  return new_sc


def swap_origin(i, scanner):
  new_sc = []
  for j in range(len(scanner)):
    new_sc.append(subtract(scanner[j], scanner[i]))
  return new_sc


def subtract(a, b):
  return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
  return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def manhattan_dist(a, b):
  return sum([abs(a[0]-b[0]), abs(a[1] - b[1]), abs(a[2] - b[2])])


def rotate(coord):
  x, y, z = coord
  r = []
  r.append((x, y, z))
  r.append((x, -z, y))
  r.append((x, -y, -z))
  r.append((x, z, -y))
  r.append((-x, -y, z))
  r.append((-x, z, y))
  r.append((-x, y, -z))
  r.append((-x, -z, -y))

  r.append((y, z, x))
  r.append((y, -x, z))
  r.append((y, -z, -x))
  r.append((y, x, -z))
  r.append((-y, -z, x))
  r.append((-y, x, z))
  r.append((-y, z, -x))
  r.append((-y, -x, -z))

  r.append((z, x, y))
  r.append((z, -y, x))
  r.append((z, -x, -y))
  r.append((z, y, -x))
  r.append((-z, -x, y))
  r.append((-z, y, x))
  r.append((-z, x, -y))
  r.append((-z, -y, -x))

  return r


def input_processing(content):
  blocks = content.strip().split('\n\n')
  scanners = []
  for block in blocks:
    scanner = []
    for line in block.strip().split('\n')[1:]:
      parts = line.strip().split(',')
      coord = (int(parts[0]), int(parts[1]), int(parts[2]))
      scanner.append(coord)
    scanners.append(scanner)
  return scanners


if __name__ == '__main__':
  f = open('input.txt')
  scanners = input_processing(f.read())
  # for s in scanners:
  #   print(s)
  #   print("*" * 10)

  res = solve(scanners)
  print(res)
