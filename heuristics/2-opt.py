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

def distancePoints(p1, p2):
  return math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2)

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

def makePathCoordinates(points, path, pathX, pathY):
  for i in range(len(path)):
    pathX[i] = points[path[i]].x
    pathY[i] = points[path[i]].y  


def isSwapBetter(points, path, i, j):
  if (i == len(points)-1): return False

  if(i > j):
    aux = i
    i = j
    j = aux

  if(j == len(points)-1): 
    initialDistance = distancePoints(points[path[i]], points[path[i+1]]) + distancePoints(points[path[j]], points[path[0]])
    swapDistance = distancePoints(points[i], points[j]) + distancePoints(points[i+1], points[0])
  else: 
    initialDistance = distancePoints(points[path[i]], points[path[i+1]]) + distancePoints(points[path[j]], points[path[j+1]])
    swapDistance = distancePoints(points[path[i]], points[path[j]]) + distancePoints(points[path[i+1]], points[path[j+1]])
  if (swapDistance < initialDistance):
    return True
  else:
    return False


# Execute the swap
# i, j: positions to swap
# n: total quantity
def swapPaths(path, i, j, n):
  if (i > j):
    aux = i
    i = j
    j = aux

  if (i <= 0 and j >= n-1): return
  
  auxList = list()
  for k in range(i+1, j+1):
    auxList.append(path[k])

  for k in range(i+1, j+1):
    path[k] = auxList.pop()

def calculateTotalCost(path, points):
  totalCost = 0
  for i in range(len(path)-1):
    totalCost += distancePoints(points[path[i]], points[path[i+1]])

  return totalCost

def main():
  start_time = time.time()*1000
  FILE = 'djibouti'
  costs, points = readFile(FILE + ".tsp") #costs and point coordinates
  num_galaxies = len(costs)
  edge = {} # edge[i, j] = 1 when there is an edge from i to j

  for i in range(num_galaxies):
    for j in range(num_galaxies):
      edge[i, j] = 0

  # Implementing greedy heuristic
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

  # Implementing 2-opt heuristic
  for i in range (len(points)):
    for j in range(len(points)):
      if(isSwapBetter(points, path, i, j)):
        swapPaths(path, i, j, num_galaxies)

  makePathCoordinates(points, path, pathX, pathY)

  totalCost = calculateTotalCost(path, points)

  # Print solution
  print('Total cost = ', totalCost, '\n')
  f = open("./solver_solutions/"+FILE+"_2_opt.sol", "w")
  for i in range(num_galaxies):
    f.write(str(path[i]) + " " + str(path[i+1]) + "\n")

  f.close()

  # Plot
  plt.plot(pathX, pathY, 'bo-', zorder=2)
  # plt.axis('off')
  plt.show()

  

  milliseconds = time.time()*1000 - start_time
  print("Execution time:", milliseconds/1000, "s")

if __name__ == "__main__":
    main()