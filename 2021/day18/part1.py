import math


# https://adventofcode.com/2021/day/18
def solve(numbers):
  result = numbers[0]
  for number in numbers[1:]:
    result = add_number(result, number)
    result = reduce_number(result)
  print(check_explode(result))
  return calculate_mag(result)


def add_number(a, b):
  return '[' + a + ',' + b + ']'


def reduce_number(number):
  next_number = None
  i = 0
  while True:
    # if i == 33:
    #   break
    i+= 1
    next_number = check_explode(number)
    if next_number != number:
      number = next_number
      # print("explode", number)
      continue
    next_number = check_split(next_number)
    # print("after", number, next_number)
    if next_number != number:
      number = next_number
      # print("split", number)
      continue
    break
  return number


def check_explode(number):
  s = []
  i = 0
  while i < len(number):
    if number[i] == ']':
      s.pop()  # get out of current level
    if number[i] == '[':
      if s.count('[') >= 4 and is_a_pair(number, i):
        # Here is the pair in the level 5, explode it
        left, j = read_int(number, i+1)
        right, j = read_int(number, j+1)

        number = number[:i] + '0' + number[j+1:]  # replace pair by 0

        j, k = i-1, i+2  # skip 0 which is just replace current pair
        while j >= 0:
          if number[j].isnumeric():
            num, l = read_int_reversed(number, j)
            number = number[:l+1] + str(num + left) + number[j+1:]
            break
          j -= 1
        while k < len(number):
          if number[k].isnumeric():
            num, l = read_int(number, k)
            number = number[:k] + str(num + right) + number[l:]
            break
          k += 1
        break
      else:
        s.append(number[i])
    i += 1
  return number


def check_split(number):
  i = 0
  while i < len(number):
    if number[i].isnumeric():
      num, j = read_int(number, i)
      if num >= 10:
        number = number[:i] + '[' + str(math.floor(num / 2.0)) + \
            ',' + str(math.ceil(num / 2.0)) + ']' + number[j:]
        break
      i = j
    else:
      i += 1
  return number


def read_int(number, i):
  num = ''
  while number[i].isnumeric():
    num += number[i]
    i += 1
  return int(num), i


def read_int_reversed(number, i):
  num = ''
  while number[i].isnumeric():
    num = number[i] + num
    i -= 1
  return int(num), i


def calculate_mag(number):
  val = []
  i = 0
  while i < len(number):
    if number[i].isnumeric():
      num, i = read_int(number, i)
      val.append(num)
    if number[i] == ']':
      val.append(2 * val.pop() + 3 * val.pop())
    i += 1
  return val[0]


def is_a_pair(number, i):
  if number[i] != '[':
    return False
  if not number[i+1].isnumeric():
    return False
  num, j = read_int(number, i+1)
  if number[j+1].isnumeric():
    return True
  return False


def input_processing(content):
  return [line.strip() for line in content.strip().split('\n')]
  # numbers = []
  # for line in content.strip().split('\n'):
  #   number = parse_line(line.strip())
  #   numbers.append(number)
  # return numbers

def parse_line(line):
  number = []
  i = 1 # skip two bracket in outmost level
  while line[i] != ']':
    if line[i] == '[':
      pair, i = parse_pair(line, i)
      number.append(pair)
    elif line[i] == ',':
      i += 1
    else:
      number.append(int(line[i]))
      i += 1
  return number

def parse_pair(line, i):
  pair = []
  i += 1  # open bracket
  while line[i] != ']':
    if line[i] == '[':
      sub_pair, i = parse_pair(line, i)
      pair.append(sub_pair)
    elif line[i] == ',':
      i += 1
    else:
      pair.append(int(line[i]))
      i += 1
  return pair, i+1  # close bracket


if __name__ == '__main__':
  f = open('input.txt')
  numbers = input_processing(f.read())
  for number in numbers:
    print(number)
  print("*" * 10)

  res = solve(numbers)
  print(res)
