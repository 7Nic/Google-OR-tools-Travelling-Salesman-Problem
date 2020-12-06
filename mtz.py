# Miller tuker zemlim formulation
from ortools.linear_solver import pywraplp
import numpy as np
import itertools
import time
import math

def mtzModel(solver, num_nodes, costs):
    # Function used to add the restrictions, variables and objective to the solver.
    # After it is executed, the Miller-Tuker-Zemlim formulation is modeled into the solver
     # PARAMS
    # solver   -> instance of ortools.linear_solver.Solver
    # num_nodes-> number of nodes in the problem
    # costs    -> costs matrix of the problem
    # RETURNS
    # x -> dict of variables not involved in subtour avoiding restrictions (tuple to ortools.linear_solver.Variable)
    x = {} #this is returned
    u = {} #this is not
    inf = solver.infinity()
    for i in range(num_nodes):
        if (i != 0): 
            u[i] = solver.NumVar(-inf, inf, '')

        for j in range(num_nodes):
            x[i, j] = solver.IntVar(0, 1, '')

    for i in range(num_nodes):
        list1 = []
        for j in range(num_nodes):
            if (i != j): list1.append(x[i, j])
        solver.Add(solver.Sum(list1) == 1)

    for j in range(num_nodes):
        list2 = []
        for i in range(num_nodes):
            if (i != j): list2.append(x[i, j])
        solver.Add(solver.Sum(list2) == 1)
    
    for i in range(1, num_nodes):
        solver.Add(u[i] >= 1)
        solver.Add(u[i] <= num_nodes-1)


    node_list = list()
    for i in range(1, num_nodes):
        node_list.append(i)        

    subsets = set(itertools.combinations(node_list,2))
    for subset in subsets:
        i = subset[0]
        j = subset[1]
        solver.Add(u[i] - u[j] + (num_nodes*x[i,j]) <= num_nodes - 1)
        solver.Add(u[j] - u[i] + (num_nodes*x[j,i]) <= num_nodes - 1) # Because j will always be greater than i
    
    # Objective
    objective_terms = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            objective_terms.append(costs[i][j] * x[i, j])
    solver.Minimize(solver.Sum(objective_terms))

    return x

