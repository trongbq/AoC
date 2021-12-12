# https://adventofcode.com/2021/day/8
def solve(data):
  if len(data) == 0:
    return 0

  count = 0
  
  # Digits 1, 4, 7, 8 each have unique number of segments
  seek_lengths = [2, 4, 3, 7]

  for record in data:
    # We focus only on output values
    output = record[1]
    for val in output:
      if len(val) in seek_lengths:
        count += 1

  return count


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
  print(data)

  res = solve(data)
  print(res)
