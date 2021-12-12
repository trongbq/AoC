from collections import defaultdict


# https://adventofcode.com/2021/day/12
def solve(graph):
  if len(graph) == 0:
    return 0

  # Use dict to memorize small cave visited, 
  # use value as int to record a small cave can be visited twice
  small_cave_visited = {}
  for v in graph:
    if v.islower():
      small_cave_visited[v] = 0

  # traverse graph
  paths = []
  traverse(graph, 'start', paths, [], small_cave_visited)

  [print(path) for path in paths]

  return len(paths)


def traverse(graph, s, paths, path, small_cave_visited):
  path.append(s)

  if s == 'end':
    paths.append(path)
    return
  
  for v in graph[s]:
    if v == 'start':
      continue
    if v.islower():
      # Normal visit
      if small_cave_visited[v] == 0:
        small_cave_visited[v] = 1
        traverse(graph, v, paths, path.copy(), small_cave_visited)
        small_cave_visited[v] = 0
      elif small_cave_visited[v] == 1:
        # If no small cave has been visited twice, we take our chance
        if not 2 in list(small_cave_visited.values()):
          small_cave_visited[v] = 2
          traverse(graph, v, paths, path.copy(), small_cave_visited)
          small_cave_visited[v] = 1
    else:
      traverse(graph, v, paths, path.copy(), small_cave_visited)


# Use map list to present graph data
def input_processing(paths):
  graph = defaultdict(list)
  for path in paths:
    s, t = path.strip().split('-')
    graph[s].append(t)
    graph[t].append(s)
  print(graph)
  return graph


if __name__ == '__main__':
  f = open('input.txt')
  graph = input_processing(f.readlines())

  res = solve(graph)
  print(res)
