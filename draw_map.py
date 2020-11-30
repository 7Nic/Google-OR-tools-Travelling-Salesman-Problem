import matplotlib.pyplot as plt

FILE = 'djibouti.tsp'
f = open("./data/" + FILE, "r")
qttLines = int(f.readline())
xPoints = list()
yPoints = list()
for i in range(qttLines):
    line = f.readline()
    (x,y) = line.split()
    xPoints.append(float(x))
    yPoints.append(float(y))

f.close()

xPoints = [1, 2, 3, 4]
yPoints = [1, 4, 9, 16]

plt.plot(xPoints, yPoints, 'bo', zorder=2)
plt.plot([1, 3, 2, 4], [1, 9, 4, 16], 'y-', zorder=1)
# plt.axis([0, 6, 0, 20])
plt.show()