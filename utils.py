from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time
import math


INF = 10000000000
PERCENTAGE = 50

# Calculate distances
def readGraph(file):
    # Takes the input file and returns a costs matrix and the list of read points
    # PARAMS
    # file  -> name of the file
    # RETURNS
    # distances -> costs matrix
    # points -> list of points

    f = open("./data/" + file, "r")
    qttLines = int(f.readline())
    distances = np.zeros([qttLines, qttLines], dtype=float)
    points = []
    for i in range(qttLines):
        line = f.readline()
        (x, y) = line.split()
        x = float(x)
        y = float(y)
        points.append((x, y))

    for i in range(qttLines):
        for j in range(qttLines):
            if (i == j):
                distances[i][j] = INF
                continue
            distances[i][j] = distance(
                points[i][0], points[i][1], points[j][0], points[j][1])

    f.close()
    return distances, points



def sortKey(e):
    return e[2]

def readHeuristicsGuloso(fileName, solver, modelVars, costs, num_nodes):
    # Function used to add the restrictions related to the PERCENTAGE/100*num_nodes modelVars
    # that were given in the fileName solution
    # PARAMS
    # fileName -> name of the file containing the previous solution
    # solver   -> instance of ortools.linear_solver.Solver
    # modelVars-> ortools.linear_solver.Variable; variables of the model
    # num_nodes-> number of nodes in the problem
    # costs    -> costs matrix of the problem

    # Start solution
    f = open("./heuristics/solver_solutions/" + fileName, "r")
    lines = f.readlines()
    
    path = list()

    for line in lines:
        i = int(line.split()[0])
        j = int(line.split()[1])
        cost = costs[i][j]
        path.append((i, j, cost))

    path.sort(key=sortKey)

    # Adding half best values of heuristic path
    for i in range(0, int(num_nodes*PERCENTAGE/100)):
        solver.Add(modelVars[path[i][0], path[i][1]] == 1)

    f.close()



def readHeuristics(fileName, solver, modelVars, costs, num_nodes):
    # Function used to give a initial solution to the solver using the solver.SetHint method
    # PARAMS
    # fileName -> name of the file containing the previous solution
    # solver   -> instance of ortools.linear_solver.Solver
    # modelVars-> ortools.linear_solver.Variable; variables of the model
    # num_nodes-> number of nodes in the problem
    # costs    -> costs matrix of the problem

    # Start solution
    f = open("./heuristics/solver_solutions/" + fileName, "r")
    lines = f.readlines()

    path = list()
    
    for line in lines:
        i = int(line.split()[0])
        j = int(line.split()[1])
        cost = costs[i][j]
        path.append((i, j, cost))

    hint_val = []
    hint = []
    is_in_hint = {}
    for var in modelVars:
        is_in_hint[modelVars[var]] = False

    for i in range(0, num_nodes):
        hint.append(modelVars[path[i][0], path[i][1]])
        hint_val.append(1)
        is_in_hint[modelVars[path[i][0], path[i][1]]] = True
    
    for var in modelVars:
        if not is_in_hint[modelVars[var]]:
            hint.append(modelVars[var])
            hint_val.append(False)
            is_in_hint[modelVars[var]] = True

    solver.SetHint(hint, hint_val)

    f.close()




def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
