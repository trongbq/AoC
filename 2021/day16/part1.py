table = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
  }

# https://adventofcode.com/2021/day/16
def solve(hexstr):
  binstr = ''.join([table[c.lower()] for c in hexstr])

  packet, _ = parse(binstr, 0)
      
  print(packet)

  return sum_version(packet)


def parse(binstr, i):
  pi = i
  version = int(binstr[i:i+3], 2)
  i += 3

  type_id = int(binstr[i:i+3], 2)
  i += 3

  if type_id == 4:
    value, i = literal_value(binstr, i)
  else:
    value, i = operator(binstr, i)

  return (version, type_id, value), i


def literal_value(binstr, i):
  last = False
  value = ''

  while not last:
    value += binstr[i+1:i+5]
    if binstr[i] == '0':
      last = True
    i += 5

  return int(value, 2), i


def operator(binstr, i):
  length_type_id = binstr[i]
  i += 1
  if length_type_id == '0':
    l = int(binstr[i:i+15], 2)
    i += 15
    return parse_size(binstr, i, l)
  else:
    c = int(binstr[i:i+11], 2)
    i += 11
    return parse_mul(binstr, i, c)


def parse_size(binstr, i, l):
  limit = i + l
  packets = []
  while i < limit:
    sub_repr, i = parse(binstr, i)
    packets.append(sub_repr)

  return packets, i


def parse_mul(binstr, i, c):
  packets = []
  for _ in range(c):
    packet, i = parse(binstr, i)
    packets.append(packet)
  return packets, i


def sum_version(packet):
  if type(packet) is list:
    return sum([sum_version(it) for it in packet])

  ver, typ, val = packet

  if type(val) is int:
    return ver

  return ver + sum_version(val)


if __name__ == '__main__':
  f = open('input.txt')

  res = solve(f.read().strip())
  print(res)
