from collections import defaultdict


# https://adventofcode.com/2021/day/14
def solve(template, replacements, steps):
  for s in range(0, steps):
    i = 0
    while (i < len(template)-1):
      # Move two characters at a time and check for replacement
      pair = template[i:i+2]
      if pair in replacements:
        template = template[:i+1] + replacements[pair] + template[i+1:]
        i += 2
      else:
        i += 1
    print(s, template)

  freq_map = defaultdict(lambda: 0)
  for c in template:
    freq_map[c] += 1
  freq = list(freq_map.values())

  return max(freq) - min(freq)


def input_processing(content):
  template, remain = content.split('\n\n')

  steps = {}
  for line in remain.strip().split('\n'):
    a, b = line.split('->')
    steps[a.strip()] = b.strip()

  return template.strip(), steps


if __name__ == '__main__':
  f = open('input.txt')
  template, replacements = input_processing(f.read())
  print(template)
  print(replacements)

  res = solve(template, replacements, 10)
  print(res)
