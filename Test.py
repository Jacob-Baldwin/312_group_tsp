from TSPClasses import *
from TSPSolver import TSPSolver
import Proj5GUI

import random
import csv
import time

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

data_range = {'x': [-1.5, 1.5], 'y': [-1.0, 1.0]}
diff = "Hard (Deterministic)"

def newPoints(seed, npoints):
  random.seed( seed )

  ptlist = []
  RANGE = data_range
  xr = data_range['x']
  yr = data_range['y']
  while len(ptlist) < npoints:
    x = random.uniform(0.0,1.0)
    y = random.uniform(0.0,1.0)
    if True:
      xval = xr[0] + (xr[1]-xr[0])*x
      yval = yr[0] + (yr[1]-yr[0])*y
      ptlist.append( QPointF(xval,yval) )
  return ptlist

def generateNetwork(seed, n):
  points = newPoints(seed, n) # uses current rand seed
  rand_seed = seed
  scenario = Scenario( city_locations=points, difficulty=diff, rand_seed=rand_seed )

  return scenario


numbers = [15, 30, 60, 100, 200, 300]
# numbers = [15, 20]
seeds = [101, 202, 303, 404, 505, 606]
# seeds = [20, 121]
MAX_TIME = 600

results = []

filename = "testoutput_" + str(int(time.time())) + ".csv"

csvfile = open(filename, 'w', newline='')
csvwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

csvwriter.writerow(['n,','seed,', 'random_time,', 'random_cost,', 'greedy_time,', 'greedy_cost,', 'bb_time,', 'bb_cost,', 'gen_time,', 'gen_cost,'])

n_test_sets = len(seeds) * len(numbers)

i = 0
for n in numbers:
  for seed in seeds:
    i += 1
    scenario = generateNetwork(seed, n)
    solver = TSPSolver(None)
    solver.setupWithScenario(scenario)

    print("test set", i, "of", n_test_sets)
    print("seed", seed)
    print("n", n)
    ran_result = solver.defaultRandomTour(time_allowance=MAX_TIME)
    greedy_result = solver.greedy(time_allowance=MAX_TIME)
    bb_result = solver.branchAndBound(time_allowance=MAX_TIME)
    gen_result = solver.fancy(time_allowance=MAX_TIME)

    row = []
    row.append(n)
    row.append(',')
    row.append(seed)
    row.append(',')
    row.append(ran_result['time'])
    row.append(',')
    row.append(ran_result['cost'])
    row.append(',')
    row.append(greedy_result['time'])
    row.append(',')
    row.append(greedy_result['cost'])
    row.append(',')
    row.append(bb_result['time'])
    row.append(',')
    row.append(bb_result['cost'])
    row.append(',')
    row.append(gen_result['time'])
    row.append(',')
    row.append(gen_result['cost'])

    print(row)
    csvwriter.writerow(row)



csvfile.close()
