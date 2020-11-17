import numpy as np
import math

def distance(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# f = open("./data/teste.tsp", "r")
f = open("./data/qatar.tsp", "r")
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
      distances[i][j] = 100000000000
      continue

    distances[i][j] = distance(points[i][0],points[i][1],points[j][0],points[j][1])

print(distances)