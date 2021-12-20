# https://adventofcode.com/2021/day/20#part2
def solve(code, image):
  # Use dict to store list of position that are `#` for instant access
  mem = {}
  for i in range(len(image)):
    for j in range(len(image[0])):
      if image[i][j] == '#':
        mem[(i, j)] = 1
  
  N = len(image)
  iteration = 50
  # Assume infinite image with boundary is 10,
  # enough for the input when code[0] and code[511] cancel each other after even iteration
  extra = iteration*2

  for k in range(iteration):
    nmem = {}
    for i in range(-extra, N+extra):
      for j in range(-extra, N+extra):
        bstr = form_binary(i, j, mem)
        num = int(bstr, 2)
        c = code[num]
        if c == '#':
          nmem[(i, j)] = 1
    mem = nmem

  # matrix = [['#' if (i,j) in mem else '.' for j in range(-extra, N+extra)] for i in range(-extra,N+extra)]
  # [print(''.join(row)) for row in matrix]
  # print("---")
      
  # Count number of `#` and skip outmost borders because it's redundant calculation
  # Each iteration just add 1 more extra
  c = 0
  for i in range(-iteration, N+iteration):
    for j in range(-iteration, N+iteration):
      if (i, j) in mem:
        c += 1
  return c


def form_binary(i, j, mem):
  s = ''
  for a in range(-1, 2):
    for b in range(-1, 2):
      s += '1' if (i+a, j+b) in mem else '0'
  return s


def input_processing(content):
  blocks = content.strip().split('\n\n')
  code = blocks[0].strip()
  image = [list(line) for line in blocks[1].strip().split('\n')]
  return code, image


if __name__ == '__main__':
  f = open('input.txt')
  code, image = input_processing(f.read())
  # print(code)
  # [print(row) for row in image]

  res = solve(code, image)
  print(res)
