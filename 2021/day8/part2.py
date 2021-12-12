from collections import defaultdict


# https://adventofcode.com/2021/day/8
def solve(data):
  if len(data) == 0:
    return 0

  four_digits = []
  for line in data:
    digit = solve_each(line[0], line[1])
    four_digits.append(digit)
  print(four_digits)
  return sum(four_digits)


def solve_each(inp, out):
  # ----1----
  # |        |
  # 2        3
  # |        |
  # ----4----
  # |        | 
  # 5        6
  # |        |
  # ----7----
  mapping = {}

  # Same digit but order different for input and output, sort it to make thing
  print(inp, out)
  inp = [''.join(sorted(val)) for val in inp]
  out = [''.join(sorted(val)) for val in out]
  print(inp, out)

  # Category input by sizes
  sizes = defaultdict(list)
  for val in inp:
    sizes[len(val)].append(val)

  # Easily mapping 4 digits which have distinct sizes
  mapping[sizes[2][0]] = 1
  mapping[sizes[3][0]] = 7
  mapping[sizes[4][0]] = 4
  mapping[sizes[7][0]] = 8

  # Remaining sizes: 
  # [5, 2, 3] have size 5
  # [0, 9, 6] have size 6

  # Start with size 5
  for val in sizes[5]:
    # Only 3 contains all segments in 1
    if contains(sizes[2][0], val):
      mapping[val] = 3
      continue
    # 5 contains what left from subtracting segments of 4 to 1
    if contains(remove(sizes[2][0], sizes[4][0]), val):
      mapping[val] = 5
      continue
    # Remaining unmatched digit must be 2
    mapping[val] = 2

  # Deduction for size 6
  for val in sizes[6]:
    # Only 9 can contains all segments of 4
    if contains(sizes[4][0], val):
      mapping[val] = 9
      continue
    # Between 0 and 6, only 0 can contains all segments of 1
    if contains(sizes[2][0], val):
      mapping[val] = 0
      continue
    # Remaining must be 6
    mapping[val] = 6
  print(mapping)
  # Mapping to output
  four_digits = []
  for val in out:
    four_digits.append(mapping[val])
  print(four_digits)
  a = int(''.join([str(d) for d in four_digits]))
  if a == 9219:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.")
  print('')

  return int(''.join([str(d) for d in four_digits]))


# Check if all segments in a also in b
def contains(a, b):
  exist = {}
  for val in b:
    exist[val] = 1
  
  for val in a:
    if val not in exist:
      return False
  return True

# Remove all segments of a that in b
def remove(a, b):
  new_b = []
  for val in b:
    if val not in a:
      new_b.append(val)
  return ''.join(new_b)


def input_processing(lines):
  output = []
  # Separate each line into two parts, input and output
  for line in lines:
    a, b = line.split('|')
    output.append([[code.strip() for code in a.split()], [code.strip() for code in b.split()]])

  return output


if __name__ == '__main__':
  f = open('input.txt')
  data = input_processing(f.readlines())

  res = solve(data)
  print(res)
