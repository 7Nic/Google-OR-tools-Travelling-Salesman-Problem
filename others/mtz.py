# Miller tuker zemlim formulation
from ortools.linear_solver import pywraplp
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

    return distances

def main():
    start_time = time.time()*1000
    solver = pywraplp.Solver.CreateSolver('SCIP')
    
    INFINITY = solver.infinity()


    costs = readFile('qatar.tsp')
    # costs = [[INF, 100, 125, 100,75],
    # [100, INF, 50, 75, 125],
    # [125, 50, INF, 100, 125],
    # [100, 75, 100, INF, 50],
    # [75, 125, 125, 50, INF]]
    num_galaxies = len(costs)

    x = {}
    u = {}
    for i in range(num_galaxies):
        if (i != 0): 
            u[i] = solver.NumVar(-INFINITY, INFINITY, '')

        for j in range(num_galaxies):
            x[i, j] = solver.IntVar(0, 1, '')

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
    
    for i in range(1, num_galaxies):
        solver.Add(u[i] >= 1)
        solver.Add(u[i] <= num_galaxies-1)


    node_list = list()
    for i in range(1, num_galaxies):
        node_list.append(i)        

    subsets = set(itertools.combinations(node_list,2))
    for subset in subsets:
        i = subset[0]
        j = subset[1]
        solver.Add(u[i] - u[j] + (num_galaxies*x[i,j]) <= num_galaxies - 1)
        solver.Add(u[j] - u[i] + (num_galaxies*x[j,i]) <= num_galaxies - 1) # Because j will always be greater than i
    
    # Objective
    objective_terms = []
    for i in range(num_galaxies):
        for j in range(num_galaxies):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    # Exportar modelo
    # print("Exportando modelo...")
    # model = solver.ExportModelAsLpFormat(True)
    # f = open(r"./qatar_mtz.lp","w+") 
    # f.write(model)
    # f.close()
    # return

    # Solve
    print("Iniciando a resolução...")
    minutes = 10*60*1000
    seconds = 20*1000
    solver.set_time_limit(minutes) # Time in ms
    status = solver.Solve()
    print('Acabou de resolver')

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
    print("Execution time:", milliseconds/1000, "s")

if __name__ == "__main__":
    main()