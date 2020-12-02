# Sherali and driscoll formulation
import matplotlib.pyplot as plt
import numpy as np
import time
import math

class Point:
  visited = False
  x = 0
  y = 0

  def __init__(self, x, y):
    self.x = x
    self.y = y


def distance(x1,y1,x2,y2):
  return math.sqrt((x1-x2)**2 + (y1-y2)**2)

# Calculate distances
def readFile(file):
  f = open("../data/" + file, "r")
  qttLines = int(f.readline())
  distances = np.zeros([qttLines,qttLines], dtype=float)
  points = []
  for i in range(qttLines):
      line = f.readline()
      (x,y) = line.split()
      x = float(x)
      y = float(y)
      point = Point(x, y)
      points.append(point)

  for i in range(qttLines):
      for j in range(qttLines):
          if (i == j):
              distances[i][j] = math.inf
              continue
          distances[i][j] = distance(points[i].x,points[i].y,points[j].x,points[j].y)

  f.close()
  return distances, points

def getClosestPoint(points, pointNumber, edge, num_galaxies):
  curPoint = points[pointNumber]
  closestPoint = 0
  smallerDistance = math.inf
  for i in range (num_galaxies):
    curDistance = distance(curPoint.x, curPoint.y, points[i].x, points[i].y)
    if (points[i].visited == False and curDistance < smallerDistance):
      closestPoint = i
      smallerDistance = curDistance

  return closestPoint, smallerDistance


def main():
  start_time = time.time()*1000
  FILE = 'uruguay.tsp'
  costs, points = readFile(FILE) #costs and point coordinates
  num_galaxies = len(costs)
  edge = {} # edge[i, j] = 1 when there is an edge from i to j

  for i in range(num_galaxies):
    for j in range(num_galaxies):
      edge[i, j] = 0

  # Implementing heuristic
  totalCost = 0
  curPoint = 0
  pathX = [points[curPoint].x]
  pathY = [points[curPoint].y]
  points[curPoint].visited = True
  path = [0]
  for i in range(num_galaxies-1):
    closestPoint, closestdDistance = getClosestPoint(points, curPoint, edge, num_galaxies)
    curPoint = closestPoint
    points[curPoint].visited = True
    totalCost += closestdDistance
    path.append(curPoint)
    pathX.append(points[curPoint].x)
    pathY.append(points[curPoint].y)

  # Last edge returning to node 0
  path.append(0)
  pathX.append(points[0].x)
  pathY.append(points[0].y)
  totalCost += distance(points[curPoint].x, points[curPoint].y, points[0].x, points[0].y)



  # Print solution
  print('Total cost = ', totalCost, '\n')
  pathStr = ""
  f = open("uy734.sol", "w")
  f.write("Ordem de visita dos vértices\n")
  for point in path:
    pathStr = pathStr + "-->" + str(path[point]+1) # +1 to start in node 1
    f.write(str(path[point]+1) + "\n")
  print(pathStr)
  f.close()

  plt.plot(pathX, pathY, 'bo-', zorder=2)
  plt.axis('off')
  plt.show()

  

  milliseconds = time.time()*1000 - start_time
  print("Execution time:", milliseconds/1000, "s")

if __name__ == "__main__":
    main()