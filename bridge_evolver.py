from bridgelib2 import *
import math as math
import random as random
from tqdm import tqdm


mandatory_length = 1280
b1 = Bridge(1.27, 100.54, mandatory_length, 105, 2, 2, 1, 55, 91.45)

list_of_bearing = []

for i in range(1):
	b_final = evolve(b1, 100000)
	print("B_Final Paper Usage: ",b_final.get_amount_paper())
	list_of_bearing.append(b_final.get_max_load())

print(list_of_bearing)

b_final.report()