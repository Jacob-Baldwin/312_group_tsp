from TSPClasses import TSPSolution

import numpy as np
import random
import time

class GeneticSolver():
  def __init__(self, cities, timeout=4, n_initial_solutions=100, population_size=100):
    # set self variables for cities, timeout, and max_generations
    # create initial population of Solutions
    self.cities = cities
    self.timeout = timeout
    self.n_initial_solutions = n_initial_solutions
    self.solutions = []
    self.population_size = population_size
    self.best = None

    for i in range(n_initial_solutions):
      self.solutions.append(Solution().randomSolution(cities))

    new_solution = Solution().fromParents(self.solutions[0], self.solutions[1])

  def solve(self):
    # repeat iterGeneration until timeout or max_generations is reached
    # return the best scored solution
    results = {}

    start_time = time.time()
    i = 0
    timer = time.time()
    while time.time() - start_time < self.timeout:
      i += 1

      if time.time() - timer > 10:
        print("gen ", i)
        timer = time.time()

      self.iterGeneration()
      self.cull()
    end_time = time.time()

    results['cost'] = self.best.solution.cost
    results['time'] = end_time - start_time
    results['count'] = i
    results['soln'] = self.best.solution
    results['max'] = None
    results['total'] = None
    results['pruned'] = None

    print(results)

    return results

  def iterGeneration(self, breeding_percentage=0.5):
    # take all current solutions
    # pair them up
    # cross them over with their partners
    # get their fitness, rank them accordingly
    # call cull to limit population size
    sol_len = len(self.solutions) - 1

    for i in range(int(sol_len*breeding_percentage)):

      r1 = random.randint(0, sol_len)
      r2 = random.randint(0, sol_len)
      r3 = random.randint(0, sol_len)
      r4 = random.randint(0, sol_len)
      while r1 in (r2, r3, r4) or r2 in (r1, r3, r4) or r3 in (r2, r1, r4) or r4 in (r2, r3, r1):
        r1 = random.randint(0, sol_len)
        r2 = random.randint(0, sol_len)
        r3 = random.randint(0, sol_len)
        r4 = random.randint(0, sol_len)

      # r1 VS r2
      mom = self.fight(r1, r2)
      # r3 VS r4
      dad = self.fight(r3, r4)

      child = Solution().fromParents(mom, dad)

      if self.best == None or self.best.solution.cost > child.solution.cost:
        self.best = child

      self.solutions.append(child)

  def fight(self, i1, i2, chance=0.7, invert=False):
    s1 = self.solutions[i1]
    s2 = self.solutions[i2]

    r = random.random()

    if s1.solution.cost > s2.solution.cost:
      best = s2
      worst = s1
    else:
      best = s1
      worst = s2


    return_best = (r < chance)

    if invert:
      return_best = not return_best

    if return_best:
      return best
    else:
      return worst

  def cull(self):
    # keep the best solution(s) from our population
    # randomly eliminate some of the other solutions
    # we may want to have some kind of weighted algorithm
    # for deciding which solutions to keep

    while len(self.solutions) > self.population_size:
      sol_len = len(self.solutions) - 1

      r1 = random.randint(0, sol_len)
      r2 = random.randint(0, sol_len)
      while r1 == r2 or self.solutions[r1] == self.best or self.solutions[r2] == self.best:
        r1 = random.randint(0, sol_len)
        r2 = random.randint(0, sol_len)

      # r1 VS r2
      loser = self.fight(r1, r2, invert=True)

      self.solutions.remove(loser)


class Solution():
  def __init__(self, mutate_chance=0.1):
    self.sequence = []
    self.solution = None
    self.mutate_chance = mutate_chance

  def randomSolution(self, cities):
    # generates a random sequence from cities that
    # contains each city exactly once
    # gets fitness
    perm = np.random.permutation(len(cities))
    for i in perm:
      self.sequence.append(cities[i])

    self.getFitness()

    return self

  def fromParents(self, p1, p2):
    # our crossover function
    # constructs a solution from two parent solutions
    # constructs a sequence by crossing over the parent sequences
    # has a random chance of calling mutate
    # gets fitness for self

    seq_len = len(p1.sequence)

    start = random.randint(0, seq_len-1)
    end = random.randint(0, seq_len-1)

    if start > end:
      start, end = end, start

    self.sequence = [None]*seq_len

    for i in range(start, end):
      self.sequence[i] = p1.sequence[i]

    for c in p2.sequence:
      if c not in self.sequence:
        index = self.sequence.index(None)
        self.sequence[index] = c

    self.getFitness()

    if random.random() < self.mutate_chance:
      self.mutate()

    return self

  def mutate(self):
    # will randomly swap two cities in the solutions sequence
    i = random.randint(0, len(self.sequence)-1)
    j = random.randint(0, len(self.sequence)-1)

    while j == i:
      j = random.randint(0, len(self.sequence)-1)

    # SUSPECT
    self.sequence[i], self.sequence[j] = self.sequence[j], self.sequence[i]

    self.getFitness()

  def getFitness(self):
    # gets the distance of self's sequence
    # can be done with the TSPSolution class
    self.solution = TSPSolution(self.sequence)

  def __str__(self):
    output = "[ "

    for city in self.sequence:
      output += city._name + " "

    output += "]"

    output += " cost: " + str(self.solution.cost)

    return output
