from collections import defaultdict


# https://adventofcode.com/2021/day/14
def solve(template, replacements, steps):
  mapping = defaultdict(lambda: 0)
  for i in range(0, len(template)-1):
    mapping[template[i:i+2]] += 1

  for i in range(0, steps):
    new_pairs = defaultdict(lambda: 0)
    pairs = list(mapping.keys())
    # Iterate through all existing pair and find replacement
    for pair in pairs:
      if pair in replacements:
        new_pairs[pair[0] + replacements[pair]] += mapping[pair]
        new_pairs[replacements[pair] + pair[1]] += mapping[pair]
        del mapping[pair]

    # Add new pairs to existing mapping
    for pair, freq in new_pairs.items():
      mapping[pair] += freq    

  # Get frequency of each characters
  freq_map = defaultdict(lambda: 0)
  for pair, freq in mapping.items():
    freq_map[pair[0]] += freq
    freq_map[pair[1]] += freq
  freq = [freq // 2 if freq % 2 == 0 else freq // 2 + 1 for freq in freq_map.values()]

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

  res = solve(template, replacements, 40)
  print(res)
