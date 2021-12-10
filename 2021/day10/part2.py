# https://adventofcode.com/2021/day/10
def solve(lines):
  if len(lines) == 0:
    return 0

  close_mappings = {')': '(', ']': '[', '}': '{', '>': '<'}
  open_mappings = {'(': ')', '[': ']', '{': '}', '<': '>'}
  open_symbols = ['(', '[', '{', '<']
  close_symbols = [')', ']', '}', '>']

  scores = []
  for line in lines:
    stack = []
    corrupted = False
    for sym in line:
      if sym in close_symbols:
        if stack[-1] != close_mappings[sym]:
          # Corrupted  line
          corrupted = True
          break
        else:
          stack.pop()
      if sym in open_symbols:
        stack.append(sym)

    if not corrupted:    
      # Imcomplete line
      closings = []
      while stack:
        closings.append(open_mappings[stack.pop()])
      scores.append(calculate_score(closings))

  return sorted(scores)[len(scores) // 2]


def calculate_score(closings):
  score_mappings = {')': 1, ']': 2, '}': 3, '>': 4}
  score = 0
  for sym in closings:
    score *= 5
    score += score_mappings[sym]
  return score


def input_processing(content):
  return [[sym.strip() for sym in line] for line in content.split('\n')[:-1]]


if __name__ == '__main__':
  f = open('input.txt')
  lines = input_processing(f.read())

  res = solve(lines)
  print(res)
