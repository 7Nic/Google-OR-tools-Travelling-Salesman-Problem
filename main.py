from ortools.linear_solver import pywraplp
import itertools

# Create the mip solver with the SCIP backend.
solver = pywraplp.Solver.CreateSolver('SCIP')

costs = [[1000000, 100, 125, 100,75],
 [100, 1000000, 50, 75, 125],
 [125, 50, 1000000, 100, 125],
 [100, 75, 100, 1000000, 50],
 [75, 125, 125, 50, 1000000]]
num_galaxies = len(costs)

x = {}
for i in range(num_galaxies):
    for j in range(num_galaxies):
        x[i, j] = solver.IntVar(0, 1, '')

for i in range(num_galaxies):
    solver.Add(solver.Sum([x[i, j] for j in range(num_galaxies)]) == 1)

for j in range(num_galaxies):
    solver.Add(solver.Sum([x[i, j] for i in range(num_galaxies)]) == 1)

Q = set()
l = list()
for i in range(num_galaxies):
    l.append(i)

for i in range(2,num_galaxies):
    subsets = set(itertools.combinations(l,i))
    for subset in subsets:
        Q.add(subset)


for subset in Q:
    my_sum = []
    for i in subset:
        for j in subset:
            if (i != j):
                my_sum.append(x[i,j])
    solver.Add(solver.Sum(my_sum) <= len(subset) - 1)

# Objective
objective_terms = []
for i in range(num_galaxies):
    for j in range(num_galaxies):
        objective_terms.append(costs[i][j] * x[i, j])
solver.Minimize(solver.Sum(objective_terms))

# Solve
status = solver.Solve()

# Print solution.
if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
    print('Total cost = ', solver.Objective().Value(), '\n')
    for i in range(num_galaxies):
        for j in range(num_galaxies):
            # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
            if x[i, j].solution_value() > 0.5:
                print('Galaxy %d to galaxy %d.  Cost = %d' %
                     (i, j, costs[i][j]))

