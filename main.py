# Resolução de um problema do Caixeiro Viajante com o método Simplex para disciplina de Pesquisa Operacional - UFAL
# Equipe: Vanessa Vieira, Rubem Ferreira e André Santana
# Professora: Roberta Lopes


# Modelagem do problema:

# Minimizar:

# Z = 12 X1 + 4 X2 + 3 X3 + 5 X4 + 5 X5 + 3 X6 + 2 X7 + 10 X8 +
#                10 X9 + 2 X10 + 10 X11 + 10 X12 + 2 X13 + 4 X14

# Restrições:

# 1 X1 + 1 X2 + 0 X3 + 0 X4 + 0 X5 + 0 X6 + 0 X7 + 0 X8 + 0 X9 + 0 X10 + 0 X11 + 0 X12 + 0 X13 + 0 X14 = 1
# -1 X1 + 0 X2 + 1 X3 + 1 X4 -1 X5 -1 X6 + 0 X7 + 0 X8 + 0 X9 + 0 X10 + 0 X11 + 0 X12 + 0 X13 + 0 X14 = 0
# 0 X1 -1 X2 + 0 X3 + 0 X4 + 0 X5 + 0 X6 + 1 X7 + 1 X8 -1 X9 -1 X10 + 0 X11 + 0 X12 + 0 X13 + 0 X14 = 0
# 0 X1 + 0 X2 + 0 X3 -1 X4 + 1 X5 + 0 X6 -1 X7 + 0 X8 + 0 X9 + 1 X10 + 1 X11 -1 X12 + 0 X13 + 0 X14 = 0
# 0 X1 + 0 X2 -1 X3 + 0 X4 + 0 X5 + 1 X6 + 0 X7 + 0 X8 + 0 X9 + 0 X10 -1 X11 + 1 X12 + 1 X13 + 0 X14 = 0
# 0 X1 + 0 X2 + 0 X3 + 0 X4 + 0 X5 + 0 X6 + 0 X7 -1 X8 + 1 X9 + 0 X10 + 0 X11 + 0 X12 + 0 X13 + 1 X14 = 0
# 0 X1 + 0 X2 + 0 X3 + 0 X4 + 0 X5 + 0 X6 + 0 X7 + 0 X8 + 0 X9 + 0 X10 + 0 X11 + 0 X12 -1 X13 -1 X14 = -1

from scipy.optimize import linprog

c = [12, 4, 3, 5, 5, 3, 2, 10, 10, 2, 10, 10, 2, 4]

A = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [-1, 0, 1, 1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, -1, 0, 0, 0, 0, 1, 1, -1, -1, 0, 0, 0, 0], [0, 0, 0, -1, 1, 0, -1, 0, 0, 1, 1, -1, 0, 0],
     [0, 0, -1, 0, 0, 0, 0, 0, 0, 0, -1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, -1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1]]

b = [1, 0, 0, 0, 0, 0, -1]

res = linprog(c= c, A_eq= A, b_eq= b, method= 'simplex')

print(res)
