import os
import matplotlib.pyplot as plt

curPath = '.'+os.path.dirname(__file__)[len(os.path.abspath('.')):] + '/'
x_values = []
y_values = []
with open(f'{curPath}/result.txt', 'r') as f:
    data = f.readlines()
    for i,line in enumerate(data):
        x,y=line.split()
        x_values.append(float(x))
        y_values.append(float(y))
plt.plot(x_values, y_values, marker='o')
plt.show()