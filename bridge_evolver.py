from bridgelib2 import *
import math as math
import random as random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np


mandatory_length = 1280
# b1 = Bridge(1.27, 100.54, mandatory_length, 105, 2, 2, 1, 55, 91.45)
b1 = Bridge(1.27, 20.54, mandatory_length, 105, 2, 2, 1, 55, 91.45)

list_of_bearing = []
num_alphas = 1 #TODO: Define what an alpha is
legend_titles = []

for i in range(num_alphas):
	list_of_bearing.append([])

for i in range(num_alphas):
	# b_in = evolve(b1, 10000, i*4)#starting bridge, number of generation, alpha value
	b_in = evolve(b1, 100000, 20)#starting bridge, number of generation, alpha value
	b_final = b_in[0];
	list_of_bearing[i] = b_in[1];

# print(list_of_bearing)


for i in range(num_alphas):
	plt.plot(list_of_bearing[i])
	legend_titles.append('Iteration '+str(i));


#plt.legend(legend_titles)
plt.xlabel('Generation Number')
plt.ylabel('Load Bearing Ability (N)')
plt.title('Doing Some Evolution on Bridges (Asexual Reproduction)')
plt.grid(True)
plt.show();

b_final.report()

