from bridgelib2 import *
import math as math
import random as random
from tqdm import tqdm
import copy

# paper_thickness, height, length, flange_width, num_flange_layers_top, num_flange_layers_bottom, num_web_layers, web_dist, dia_dist
# b1 = Bridge(1.27, 158, 1280, 100, 2, 2, 1, 50, 107)
b1 = Bridge(1.27, 102.54, 1280, 105, 2, 2, 1, 75, 91.43)

b1.report()

b2 = copy.deepcopy(b1)
# b2 = b1

b1.height = 3000

b2.report()
