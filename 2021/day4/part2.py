# https://adventofcode.com/2021/day/4#part2
def solve(numbers, squares):
  if len(squares) == 0:
    return 0

  n = 5

  # Create a highlight memory for each square
  marked_sqrs = []
  for sqr in squares:
    marked_sqrs.append([[False] * n for i in range(0, n)])

  # Use marker to mark boards who winned
  winners = [False] * len(squares)

  # Go through each number, mark highlight and winner
  win = None
  for number in numbers:
    # Mark for number existence in each squares
    for i in range(0, len(squares)):
      # No need to update if current board winned
      if winners[i]:
        continue
      for j in range(0, n):
        for k in range(0, n):
          if squares[i][j][k] == number:
            marked_sqrs[i][j][k] = True

    # Check if any winner, first square valid to criteria is a winner
    for i in range(0, len(squares)):
      marked = marked_sqrs[i]
      square = squares[i]
      for j in range(0, n):
        if all(marked[j]) or all([row[j] for row in marked]):
          winners[i] = True
          # Check if current square is the last winnning square
          if all(winners):
            return calculate(number, square, marked)
          # Otherwise, keep searching for winner
          break

  return -1


def calculate(number, square, marked):
  s = 0
  for i in range(0, len(square)):
    for j in range(0, len(square[0])):
      if not marked[i][j]:
        s += square[i][j]
  return number * s


def input_processing(content):
  parts = content.split("\n\n")
  assert len(parts) > 2, "Malform input data"

  numbers = [int(num) for num in parts[0].split(',')]

  squares = []
  for sqr in parts[1:]:
    square = [[int(val) for val in row.strip().split()] for row in sqr.strip().split('\n')]
    squares.append(square)

  return numbers, squares


if __name__ == '__main__':
  f = open('input.txt')
  numbers, squares = input_processing(f.read())

  res = solve(numbers, squares)
  print(res)
