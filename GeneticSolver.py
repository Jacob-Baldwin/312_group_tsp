from TSPClasses import TSPSolution

class GeneticSolver():
  def __init__(self, cities, timeout=60, max_generations=100):
    # set self variables for cities, timeout, and max_generations
    # create initial population of Solutions
    pass

  def solve(self):
    # repeat iterGeneration until timeout or max_generations is reached
    # return the best scored solution
    pass

  def iterGeneration(self):
    # take all current solutions
    # pair them up
    # cross them over with their partners
    # get their fitness, rank them accordingly
    # call cull to limit population size
    pass

  def cull(self):
    # keep the best solution(s) from our population
    # randomly eliminate some of the other solutions
    # we may want to have some kind of weighted algorithm
    # for deciding which solutions to keep
    pass

  def generateInitialSolutions(self):
    pass


class Solution():
  def __init__(self):
    pass

  def randomSolution(self, cities):
    # generates a random sequence from cities that
    # contains each city exactly once
    # gets fitness
    pass

  def fromParents(self, p1, p2):
    # our crossover function
    # constructs a solution from two parent solutions
    # constructs a sequence by crossing over the parent sequences
    # has a random chance of calling mutate
    # gets fitness for self
    pass

  def mutate(self):
    # will randomly swap two cities in the solutions sequence
    pass

  def getFitness(self):
    # gets the distance of self's sequence
    # can be done with the TSPSolution class
    pass
