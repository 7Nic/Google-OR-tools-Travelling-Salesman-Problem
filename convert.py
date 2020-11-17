import numpy as np

f = open("./data/qatar.tsp", "r")
qttLines = int(f.readline())
distances = np.zeros([qttLines,qttLines], dtype=float)
points = []
print(distances)
for i in range(qttLines):
  line = f.readline()
  (x,y) = line.split()
  x = float(x)
  y = float(y)
  points.append((x,y))
  # print(x, y)

print(points)