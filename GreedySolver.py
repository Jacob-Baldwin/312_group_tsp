import copy
import numpy as np
import time
import math

from TSPClasses import TSPSolution

class GreedySolver():
  def __init__(self, cities, timeout):
    self.cities = cities
    self.timeout = timeout

  # find a greedy solution to the list of cities given
  def solve(self, starting_index):
    results = {}

    self.start_time = time.time()

    # this is where the work is done
    sequence = self.run_iteration([starting_index])

    time_elapsed = time.time() - self.start_time

    # if a solution was found create a TSPSolution object
    if sequence != None:
      city_list = []
      for i in sequence:
        city_list.append(self.cities[i])

      solution = TSPSolution(city_list)

    # if no solution was found set the solution to None
    else:
      solution = None

    results['cost'] = solution.cost if solution != None else math.inf
    results['time'] = time_elapsed
    results['count'] = 1
    results['soln'] = solution
    results['max'] = None
    results['total'] = None
    results['pruned'] = None

    return results

  # recusive function that greedily tries to cheepest edge leading to an untried city leaving from the current city
  # if that edge returns no solution try the next cheapest edge until all have been exhausted
  def run_iteration(self, sequence):
    current_index = sequence[-1]
    current_city = self.cities[current_index]
    tried_cities = []

    solution = None

    # continue the loop until we've found a solution, timedout, or tried all options
    while solution == None and len(tried_cities) + len(sequence) < len(self.cities) and time.time() - self.start_time < self.timeout:

      # find the city with the cheapest edge going to it that we haven't visited yet
      best = None
      for i in range(len(self.cities)):
        if i not in sequence and i not in tried_cities:
          if best == None and current_city.costTo(self.cities[i]) < np.inf:
            best = i
          elif best != None and current_city.costTo(self.cities[i]) < current_city.costTo(self.cities[best]):
            best = i

      # make a new sequence to pass to the next iteration of the function
      if best == None:
        return None

      new_sequence = copy.deepcopy(sequence)
      new_sequence.append(best)

      # check if we've found a tour
      # check if our new sequence includes all the cities
      if len(new_sequence) == len(self.cities):
        # check if the cost from the last city in the sequence to the first is not inf, that means we've found a tour
        # return the sequence if it is a tour but if it is inf return None
        if self.cities[new_sequence[-1]].costTo(self.cities[new_sequence[0]]) != np.inf:
          return new_sequence
        else:
          return None

      # if we haven't made a complete sequence yet run the function on the new sequence
      solution = self.run_iteration(new_sequence)

      # if a solution wasn't returned for the best index found
      # add it to the tried list and rerun the loop
      if solution == None:
        tried_cities.append(best)

    return solution
