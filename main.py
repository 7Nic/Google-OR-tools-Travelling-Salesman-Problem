from ortools.linear_solver import pywraplp
import numpy as np
import itertools
import time
import math

INF=10000000000

def distance(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

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

    return distances

def main():
    print("inicio")
    # Create the mip solver with the SCIP backend.
    start_time = time.time()*1000
    solver = pywraplp.Solver.CreateSolver('SCIP')

    costs = readFile('qatar.tsp')
    # costs = [[INF, 100, 125, 100,75],
    # [100, INF, 50, 75, 125],
    # [125, 50, INF, 100, 125],
    # [100, 75, 100, INF, 50],
    # [75, 125, 125, 50, INF]]
    num_galaxies = len(costs)

    print("comecando o pimeiro for")
    x = {}
    for i in range(num_galaxies):
        print("1")
        for j in range(num_galaxies):
            print("2")
            x[i, j] = solver.IntVar(0, 1, '')

    for i in range(num_galaxies):
        print("3")
        solver.Add(solver.Sum([x[i, j] for j in range(num_galaxies)]) == 1)
        print("4")

    for j in range(num_galaxies):
        print("5")
        solver.Add(solver.Sum([x[i, j] for i in range(num_galaxies)]) == 1)
        print("6")

    Q = set()
    l = list()
    for i in range(num_galaxies):
        print("7")
        l.append(i)

    for i in range(2,num_galaxies):
        print("8")
        subsets = set(itertools.combinations(l,i))
        for subset in subsets:
            print("9")
            Q.add(subset)

    for subset in Q:
        print("10")
        my_sum = []
        for i in subset:
            print("11")
            for j in subset:
                print("12")
                if (i != j):
                    my_sum.append(x[i,j])
        solver.Add(solver.Sum(my_sum) <= len(subset) - 1)

    # Objective
    objective_terms = []
    for i in range(num_galaxies):
        print("13")
        for j in range(num_galaxies):
            print("14")
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Solve
    print("comecando solve")
    status = solver.Solve()
    print("terminou solve")

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Total cost = ', solver.Objective().Value(), '\n')
        for i in range(num_galaxies):
            for j in range(num_galaxies):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    print('Galaxy %d to galaxy %d.  Cost = %d' %
                        (i, j, costs[i][j]))

    milliseconds = time.time()*1000 - start_time
    print("Execution time:", milliseconds, "ms")

if __name__ == "__main__":
    main()
