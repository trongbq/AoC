# https://adventofcode.com/2021/day/5
def solve(positions):
  if len(positions) == 0:
    return 0

  min_fuel = float('inf')
  min_position = -1
  
  # Try all possible positions that might take least fuel
  for i in range(min(positions), max(positions) + 1):
    temp = 0
    for p in positions:
      low, high = (p, i) if p < i else (i, p)
      temp += calculate_fuel(low, high)  # calculate required fuel to take it to position i

    if temp < min_fuel:
      min_fuel = temp
      min_position = i
        
  return min_fuel, min_position


def calculate_fuel(low, high):
  # 1 + 2 + 3 + ... + n = n(n+1)/2
  return int((1 + (high-low)) * ((high-low)/2.0))

def input_processing(content):
  return [int(val.strip()) for val in content.split(',')]


if __name__ == '__main__':
  f = open('input.txt')
  positions = input_processing(f.read())
  days = 80

  res = solve(positions)
  print(res)
