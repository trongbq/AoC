# https://adventofcode.com/2021/day/10
def solve(lines):
  if len(lines) == 0:
    return 0

  mappings = {')': '(', ']': '[', '}': '{', '>': '<'}
  score_mappings = {')': 3, ']': 57, '}': 1197, '>': 25137}
  open_symbols = ['(', '[', '{', '<']
  close_symbols = [')', ']', '}', '>']

  scores = 0
  for line in lines:
    stack = []
    for sym in line:
      if sym in close_symbols:
        if stack[-1] != mappings[sym]:
          # Corrupted
          scores += score_mappings[sym]
          break
        else:
          stack.pop()
      if sym in open_symbols:
        stack.append(sym)

  return scores


def input_processing(content):
  return [[sym.strip() for sym in line] for line in content.split('\n')[:-1]]


if __name__ == '__main__':
  f = open('input.txt')
  lines = input_processing(f.read())

  res = solve(lines)
  print(res)
