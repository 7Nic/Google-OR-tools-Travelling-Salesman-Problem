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



def readHeuristicsGuloso(fileName, solver, modelVars, costs, num_nodes):
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
    for i in range(0, int(num_nodes/2)):
        solver.Add(modelVars[path[i][0], path[i][1]] == 1)



def readHeuristics(fileName, solver, modelVars, costs, num_nodes):
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

def readSolFile(FILE, points, num_nodes):
    vars = []   
    # Creating variables
    for i in range(num_nodes):
        if (i != 0): 
          varName = "u"+str(i)
          vars.append(varName)
          # u[i] = solver.NumVar(-INFINITY, INFINITY, '') # Continuous

        for j in range(num_nodes):
          varName = "x"+" "+str(i)+" "+str(j)
          vars.append(varName)
          # x[i, j] = solver.IntVar(0, 1, varName) # Integer



    f = open(FILE, 'r')
    lines = f.readlines()

    # Old
    # for k in range(2, len(lines)):
    #   numVar = int(lines[k].split(" ")[0][1:])

    #   if (vars[numVar][0] != "x"): break

    #   # print(numVar)
    #   i = int(vars[numVar].split(" ")[1])
    #   j = int(vars[numVar].split(" ")[2])
    #   print((i, j))

    path = list()
    for k in range(2, len(lines)):
        numVar = int(lines[k].split(" ")[0][1:])

        if (vars[numVar][0] != "x"): break

        curI = int(vars[numVar].split(" ")[1])
        curJ = int(vars[numVar].split(" ")[2])
        path.append((curI, curJ))
        # print((curI, curJ))

    pathX = list()
    pathY = list()
    i = 0
    while (j != 0):
        j = path[i][1]
        print(i, j)
        pathX.append(points[i][0])
        pathY.append(points[i][1])
        i = j

    # Last edge to plot
    pathX.append(points[0][0])
    pathY.append(points[0][1])

    f.close()
    plt.plot(pathX, pathY, 'bo-', zorder=2)
    plt.axis('off')
    plt.show()
    exit()