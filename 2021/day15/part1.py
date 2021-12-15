from collections import defaultdict
import heapq

# https://adventofcode.com/2021/day/14
def solve(matrix):
  n, m = len(matrix), len(matrix[0])
  mem = [[-1] * m for _ in range(0, n)]

  return find_least_risk_path(matrix, n, m, (0, 0))


# Dijkstra
def find_least_risk_path(matrix, n, m, start):
  q = [(0, start)]
  mins = {start: 0}
  seens = set()

  while q:
    # Pop position which have lowest risk
    risk, position = heapq.heappop(q)
    if position not in seens:
      seens.add(position)
      # If this is the position we seek
      if position == (n-1, m-1):
        return risk

      x, y = position
      # Go check all of its neighbors
      for neighbor in [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]:
        xx, yy = neighbor
        if xx < 0 or xx >= n or yy < 0 or yy >= m:
          continue
        if neighbor in seens:
          continue
        # Update risk or position in the queue or set its risk if this is first time encounter
        prev_risk = mins.get(neighbor, None)
        new_risk = risk + matrix[xx][yy]
        if prev_risk is None or prev_risk > new_risk:
          mins[neighbor] = new_risk
          # There might be the case when queue have multiple items
          # point to same position with different risk level, but it not a problem
          # because we will not process any position twice with `seens` variable
          heapq.heappush(q, (new_risk, (xx, yy)))


def input_processing(content):
  return [[int(val) for val in line.strip()] for line in content.strip().split('\n')]


if __name__ == '__main__':
  f = open('input.txt')
  matrix = input_processing(f.read())

  res = solve(matrix)
  print(res)
