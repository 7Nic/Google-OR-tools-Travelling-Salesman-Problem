# Sherali and driscoll formulation
from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time
import math

INF=10000000000

def distance(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Calculate distances
def readFile(file):
  f = open("./data/" + file, "r")
  qttLines = int(f.readline())
  distances = np.zeros([qttLines,qttLines], dtype=float)
  points = []
  for i in range(qttLines):
      line = f.readline()
      (x,y) = line.split()
      x = float(x)
      y = float(y)
      points.append((x,y))

  for i in range(qttLines):
      for j in range(qttLines):
          if (i == j):
              distances[i][j] = INF
              continue
          distances[i][j] = distance(points[i][0],points[i][1],points[j][0],points[j][1])

  f.close()
  return distances, points

def main():
  start_time = time.time()*1000
  solver = pywraplp.Solver.CreateSolver('SCIP')
  INFINITY = solver.infinity()
  FILE = "djibouti"
  costs, points = readFile(FILE + '.tsp')
  num_galaxies = len(costs)

  # Model
  x = {}
  u = {}

  # Creating variables
  for i in range(num_galaxies):
    if (i != 0): 
      u[i] = solver.NumVar(-INFINITY, INFINITY, '') # Continuous

    for j in range(num_galaxies):
      x[i, j] = solver.IntVar(0, 1, '') # Integer

  # Adding initial constraints
  for i in range(num_galaxies):
    list1 = []
    for j in range(num_galaxies):
      if (i != j): list1.append(x[i, j])
    solver.Add(solver.Sum(list1) == 1)

  for j in range(num_galaxies):
    list2 = []
    for i in range(num_galaxies):
      if (i != j): list2.append(x[i, j])
    solver.Add(solver.Sum(list2) == 1)

  # DL - subtour elimination
  node_list = list()
  for i in range(1, num_galaxies):
    node_list.append(i)
    list1 = list()
    list2 = list()
    for j in range(1, num_galaxies):
      list1.append(x[j, i])
      list2.append(x[i, j])
    
    solver.Add(1 + (num_galaxies-3)*x[i, 0] + solver.Sum(list1) <= u[i] <= num_galaxies - 1 - (num_galaxies-3)*x[0, i] - solver.Sum(list2)).set_is_lazy(True) 
    # solver.Add(u[i] <= num_galaxies - 1 - (num_galaxies-3)*x[1,i] - solver.Sum(list2))

  subsets = set(itertools.combinations(node_list, 2))
  for subset in subsets:
    i = subset[0]
    j = subset[1]
    solver.Add(u[i] - u[j] + (num_galaxies-1)*x[i, j] + (num_galaxies-3)*x[j, i] <= num_galaxies - 2).set_is_lazy(True) 

    # Itertools always give subset[1] greater than subset[0]
    i = subset[1]
    j = subset[0]
    solver.Add(u[i] - u[j] + (num_galaxies-1)*x[i, j] + (num_galaxies-3)*x[j, i] <= num_galaxies - 2).set_is_lazy(True)  
  
  # Objective
  objective_terms = []
  for i in range(num_galaxies):
    for j in range(num_galaxies):
      objective_terms.append(costs[i][j] * x[i, j])
  solver.Minimize(solver.Sum(objective_terms))

  # Start solution
  # f = open("./heuristics/solver_solutions/" + FILE + "_greedy.sol", "r")
  f = open("./heuristics/solver_solutions/" + FILE + "_2_opt.sol", "r")
  lines = f.readlines()
  k = 0
  for line in lines:
    i = int(line.split()[0])
    j = int(line.split()[1])
    solver.setHint(x[i, j] == 1)
    k += 1
    # if (k > num_galaxies/2): break
  f.close()


  # Export model
  print("Exportando modelo...")
  model = solver.ExportModelAsLpFormat(True)
  f = open(r"./models/"+ FILE +"_dl.lp","w+") 
  f.write(model)
  f.close()
  return

  # Solving
  print("Starting...")
  minutes = 10*60*1000
  seconds = 20*1000
  solver.set_time_limit(minutes) # Time in ms
  status = solver.Solve()
  print('Finished')

  # Print solution
  pathX = list()
  pathY = list()
  if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print('Total cost = ', solver.Objective().Value(), '\n')

    i = 0
    # pathX.append(points[i][0])
    # pathY.append(points[i][1])

    # Iterate num_galaxies times
    for k in range(num_galaxies):
      for j in range(num_galaxies):
        # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
        if x[i, j].solution_value() > 0.5: 
          pathX.append(points[i][0])
          pathY.append(points[i][1])
          print('Galaxy %d to galaxy %d.  Cost = %d' % (i, j, costs[i][j]))
          i = j
          break

    plt.plot(pathX, pathY, 'bo-', zorder=2)
    plt.axis('off')
    plt.show()
  else:
    print("It's not feasible")

  milliseconds = time.time()*1000 - start_time
  print("Execution time:", milliseconds/1000, "s")

if __name__ == "__main__":
    main()