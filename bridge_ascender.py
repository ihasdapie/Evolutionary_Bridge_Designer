from bridgelib2 import *
import math as math
import random as random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


mandatory_length = 1280
b1 = Bridge(1.27, 100.54, mandatory_length, 105, 2, 2, 1, 55, 91.45)

list_of_bearing = []

for i in range(5):
	list_of_bearing.append([])

for i in range(5):
	b_in = evolve(b1, 10000)
	b_final = b_in[0];
	list_of_bearing[i] = b_in[1];

# print(list_of_bearing)
plt.plot(list_of_bearing[0])
plt.plot(list_of_bearing[1])
plt.plot(list_of_bearing[2])
plt.plot(list_of_bearing[3])
plt.xlabel('Generation Number')
plt.ylabel('Load Bearing Ability (N)')
plt.title('Doing Some Evolution on Bridges (Asexual Reproduction)')
plt.grid(True)
plt.show();

b_final.report()

