from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time
import math


INF = 10000000000

# Calculate distances


def readGraph(file):
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

def readHeuristics(fileName, solver, modelVars, costs, num_nodes, model_var):
    # Start solution
    # f = open("./heuristics/solver_solutions/" + FILE + "_greedy.sol", "r")
    f = open("./heuristics/solver_solutions/" + fileName, "r")
    lines = f.readlines()
    k = 0
    variables = list()
    values = list()
    edges = list()
    path = list()

    for line in lines:
        i = int(line.split()[0])
        j = int(line.split()[1])
        cost = costs[i][j]
        path.append((i, j, cost))

    path.sort(key=sortKey)

    # Adding half best values of heuristic path
    for i in range(0, int(num_nodes/2)):
        solver.Add(modelVars[path[i][0], path[i][1]] == 1)

    for a in range(num_nodes):
        for b in range(num_nodes):
            variables.append(model_var[i, j])
            if ((a, b) in edges):
                values.append(1)
            else:
                values.append(0)

    f.close()
    return variables, values

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
