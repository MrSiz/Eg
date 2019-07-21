import matplotlib.pyplot as plt 

y = [1.23, 1.24, 1.24, 1.25, 1.23, 1.25, 1.24, 1.25, 1.23]
y1 = [1.24, 1.25, 1.26, 1.25, 1.23, 1.24, 1.27, 1.23, 1.25]
y2 = [1.25, 1.22, 1.24, 1.23, 1.25, 1.27, 1.26, 1.24, 1.25]
x = [i for i in range(1, len(y) + 1)]
plt.plot(x, y)
plt.plot(x, y1)
plt.plot(x, y2)
plt.show()