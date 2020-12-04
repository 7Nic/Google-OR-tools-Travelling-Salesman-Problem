#  formulation
from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time
import math
import utils
import dlModel as dl

FILE = "qatar"
start_time = time.time()*1000

def main():
    #read graph
    print("Reading graph...")
    costs, points = utils.readGraph(FILE + '.tsp')
    num_galaxies = len(costs)

    #create solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    solver.EnableOutput()

    print("Creating model...")
    #create model
    modelVars = dl.dlModel(solver, num_galaxies, costs)

    print("Reading heuristic...")    
    #read heuristic solution
    variables, values = utils.readHeuristics( FILE + "_2_opt.sol" , solver, modelVars, costs, num_galaxies, modelVars)
    # variables, values = utils.readHeuristics( FILE + "_greedy.sol" , num_galaxies, modeloVars)

    solver.SetHint(variables, values)

    # ExportModel(solver)
    SolveModel(solver, num_galaxies, modelVars, costs, points)
    



def ExportModel(solver):
    # Export model
    print("Exportando modelo...")
    model = solver.ExportModelAsLpFormat(True)
    f = open(r"./models/" + FILE + "_2opt_dl.lp", "w+")
    f.write(model)
    f.close()
    return

def SolveModel(solver, num_nodes, modelVars, costs, points):
    # Solving
    print("Starting...")
    minutes = 10*60*1000 #10 minutes
    seconds = 20*1000 # 20 seconds
    solver.set_time_limit(minutes)  # Time in ms
    status = solver.Solve()
    print('Finished')

    # Print solution
    pathX = list()
    pathY = list()
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:

        i = 0
        for k in range(num_nodes):
            for j in range(num_nodes):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if modelVars[i, j].solution_value() > 0.5:
                    pathX.append(points[i][0])
                    pathY.append(points[i][1])
                    print('Node %d to node %d.  Cost = %d' %
                          (i, j, costs[i][j]))
                    i = j
                    break

        # Last edge to plot
        pathX.append(points[0][0])
        pathY.append(points[0][1])


        print('Total cost = ', solver.Objective().Value(), '\n')
        plt.plot(pathX, pathY, 'bo-', zorder=2)
        plt.axis('off')
        plt.show()
    else:
        print("It's not feasible")

    milliseconds = time.time()*1000 - start_time
    print("Total execution time:", milliseconds/1000, "s")
    
if __name__ == "__main__":
    main()