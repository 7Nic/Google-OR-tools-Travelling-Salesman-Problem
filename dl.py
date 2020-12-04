# Sherali and driscoll formulation
from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time
import math
import utils



def dlModel(solver, num_nodes, costs ):
  # Model
  x = {}
  u = {}
  inf = solver.infinity()

  # Creating variables
  for i in range(num_nodes):
    if (i != 0): 
      u[i] = solver.NumVar(-inf, inf, '') # Continuous

    for j in range(num_nodes):
      x[i, j] = solver.IntVar(0, 1, '') # Integer




  # Adding initial constraints
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

  # DL - subtour elimination
  node_list = list()
  for i in range(1, num_nodes):
    node_list.append(i)
    list1 = list()
    list2 = list()
    for j in range(1, num_nodes):
      list1.append(x[j, i])
      list2.append(x[i, j])
    
    solver.Add(1 + (num_nodes-3)*x[i, 0] + solver.Sum(list1) <= u[i] <= num_nodes - 1 - (num_nodes-3)*x[0, i] - solver.Sum(list2)).set_is_lazy(True) 
   

  subsets = set(itertools.combinations(node_list, 2))
  
  for subset in subsets:
    i = subset[0]
    j = subset[1]
    solver.Add(u[i] - u[j] + (num_nodes-1)*x[i, j] + (num_nodes-3)*x[j, i] <= num_nodes - 2).set_is_lazy(True) 

    # Itertools always give subset[1] greater than subset[0]
    i = subset[1]
    j = subset[0]
    solver.Add(u[i] - u[j] + (num_nodes-1)*x[i, j] + (num_nodes-3)*x[j, i] <= num_nodes - 2).set_is_lazy(True)  
  
  # Objective
  objective_terms = []
  for i in range(num_nodes):
    for j in range(num_nodes):
      objective_terms.append(costs[i][j] * x[i, j])
  solver.Minimize(solver.Sum(objective_terms))

  return x

