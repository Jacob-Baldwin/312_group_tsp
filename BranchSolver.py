import numpy as np
import math
import copy
import time
from TSPClasses import TSPSolution

class BranchSolver():
  def __init__(self, cities, time_allowance=60.0):
    self.cities = cities
    self.bssf = None
    self.pq = PQ()
    self.root = None
    self.time_allowance = time_allowance
    self.solutions = []
    self.n_states = 0
    self.n_pruned = 0

  # find either an optimal solution or keep running computation until time_allowance is reached
  # O(n!) time
  # O(n!) space
  def solve(self, start_index):
    self.root = Node(solver=self).fromCities(self.cities)
    self.root.index = start_index

    self.pq.insert(self.root)

    start_time = time.time()

    while len(self.pq) > 0 and time.time() - start_time < self.time_allowance:
      node = self.pq.pop()
      self.n_states += 1

      # prune the node if its lower bound is greater than the bssf
      if self.bssf != None and node.lower_bound >= self.bssf.cost:
        self.n_pruned += 1
        continue

      new_node = None

      # check for edges leading away from the current node and add them to the pq
      for i in range(len(node.matrix)):
        if node.matrix[node.index][i] != np.inf:
          new_node = Node().fromNode(node, i)
          self.pq.insert(new_node)

      # if there are no more paths left to explore this means we've found a possible solution
      # we're going to check it for completeness and check it against the bssf
      if new_node == None:
        route = node.getCityBacktrace()

        # make sure that all cities are present on the route
        # if not don't consider it as a solution beacause we've just hit a dead end
        if len(route) == len(self.cities):
          solution = TSPSolution(route)
          self.solutions.append(solution)

          if self.bssf is None or solution.cost < self.bssf.cost:
            self.bssf = solution
            self.n_pruned += self.pq.prune(self.bssf)

    time_elapsed = time.time() - start_time

    results = {}
    results['cost'] = self.bssf.cost if self.bssf else math.inf
    results['time'] = time_elapsed
    results['count'] = len(self.solutions)
    results['soln'] = self.bssf
    results['max'] = self.pq.max_size
    results['total'] = self.n_states
    results['pruned'] = self.n_pruned

    return results

class Node():
  def __init__(self, solver=None):
    self.cost = 0
    self.lower_bound = 0
    self.matrix = None
    self.original_matrix = None
    self.previous_node = None
    self.index = None
    self.solver = solver
    self.level = None

  # create a root node from a list of cities
  def fromCities(self, cities):
    self.cities = cities
    self.level = 0

    matrix = []

    for i, c1 in enumerate(cities):
      row = []
      for j, c2 in enumerate(cities):
        if i == j:
          row.append(np.inf)
        else:
          row.append(c1.costTo(c2))
      matrix.append(row)

    self.matrix = matrix

    self.original_matrix = copy.deepcopy(self.matrix)

    self.reduce()

    return self

  # create a leaf node from a parent node
  # takes as arguents the source node as well as the index of the city that
  # this node represents
  def fromNode(self, source_node, dest_index):
    self.index = dest_index
    self.original_matrix = source_node.original_matrix
    self.matrix = copy.deepcopy(source_node.matrix)
    self.cost = source_node.cost
    self.lower_bound = source_node.lower_bound
    self.previous_node = source_node
    self.addEdge(source_node.index, dest_index)
    self.cities = source_node.cities
    self.solver = source_node.solver
    self.level = source_node.level + 1

    return self

  def __str__(self):
    output = ""

    output += "index: " + str(self.index) + "\n"
    output += "cost: " + str(self.cost) + "\n"
    output += "lower_bound: " + str(self.lower_bound) + "\n"

    for row in self.matrix:
      for i in row:
        output += str(i) + "\t"
      output += "\n"
    return output

  # infinity out the row and column of the matrix as well as the appropriate entries
  # after adding an edge, then reduce the matrix
  # O(n**2) time
  def addEdge(self, src_index, dest_index):
    self.cost += self.original_matrix[src_index][dest_index]
    self.lower_bound += self.matrix[src_index][dest_index]

    for i in range(len(self.matrix)):
      self.matrix[i][dest_index] = np.inf
      self.matrix[src_index][i] = np.inf

    self.matrix[src_index][dest_index] = np.inf
    self.matrix[dest_index][src_index] = np.inf

    self.reduce()


  # make the reduction calculations on the reduction matrix
  # O(n**2) time
  def reduce(self):
    # reduce rows
    for row in self.matrix:
      smallest = min(row)

      if smallest != np.inf:
        self.lower_bound += smallest

      for i in range(len(row)):
        if row[i] != np.inf:
          row[i] = row[i]-smallest

    # reduce columns
    for i in range(len(self.matrix)):
      # get column min
      smallest = np.inf
      for row in self.matrix:
        if row[i] < smallest:
          smallest = row[i]

      if smallest != np.inf:
        self.lower_bound += smallest

      for row in self.matrix:
        if row[i] != np.inf:
          row[i] = row[i]-smallest

  # return a list of cities leading up to the current node for use in making a TSPSolution object
  def getCityBacktrace(self):
    output = []

    city = self.previous_node

    while city != None:
      output.append(self.cities[city.index])
      city = city.previous_node

    output.reverse()

    return output

  # return the score of the node
  # simply returns the level of the node (aka how deep it is in the tree)
  def score(self):
    return self.level

class PQ():
  def __init__(self):
    self.list = []
    self.max_size = 0

  # insert a node into the pq
  # O(1) time
  def insert(self, node):
    self.list.append(node)

    if len(self) > self.max_size:
      self.max_size = len(self)

  # remove all nodes that have a higher minimum possible cost than new_bssf.cost
  # returns the number of nodes pruned
  # O(n) time
  def prune(self, new_bssf):
    n_pruned = 0

    for n in self.list:
      if n.lower_bound >= new_bssf.cost:
        self.list.remove(n)
        n_pruned += 1

    return n_pruned

  # remove the node with the highest score from the priority queue and return in
  # O(n) time
  def pop(self):
    if len(self.list) == 0:
      return None

    best = self.list[0]

    for n in self.list:
      if n.score() > best.score():
        best = n

    self.list.remove(best)

    return best

  def __len__(self):
    return len(self.list)
