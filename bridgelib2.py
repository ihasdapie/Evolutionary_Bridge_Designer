'''c
Conditions:
	- Bridge will be the same as in the handout (double t-beam, diaphragms throughout)
	- Given variables:
		- Overall height_a
		- Overall height_b
		- Top flange width_ab
		- Bottom flange width_b
		- Distance between webs web_dist
		- Thickness of webs web_thickness
		- Thickness of top flange
		- Thickness of bottom flange
		- Overall length
		- Distance bw diaphragms
What we need to calculate:
	- Centroid location (done)
	- Moment of inertia (done)
	- Determine P value that will cause 16 MPa tensile stress @max and 6 MPa tensile stress @max (done, needs checking)
	- Determine P value that will cause 4 MPa shear stress (Done)
	- Check P for plate buckling (top flange, flex of web, shear of web) (done)
	- Check P for plate buckling (Edge of top flange!) (Done)
'''

import math as math
import random as random
from tqdm import tqdm
import copy
###CIV VARIABLES###
E = 4000
max_tensile = 30
max_compressive = 6
max_shear = 4
mu = 0.2 #poisson's ratio
max_shear_cement = 2
pi = math.pi


###CONSTRAINTS###
mandatory_length = 1280
split_point = 798 #from right to left: go from cross section A to B 
total_matboard = 813*1016 #826008

###ML VARIABLES###
aliph = 10


# Bridge of type created by group consisting of Aman, Richard, Sahil, and Mobin
class Bridge:
	def __init__(self, paper_thickness, height, length, flange_width, num_flange_layers_top, num_flange_layers_bottom, num_web_layers, web_dist, dia_dist):
		self.paper_thickness = paper_thickness
		self.height = height #webs + top flange (doesn't include bottom flange)
		self.flange_width = flange_width
		self.web_dist = web_dist
		self.length = length
		self.dia_dist = dia_dist
		self.num_flange_layers_top = num_flange_layers_top
		self.num_flange_layers_bottom = num_flange_layers_bottom
		self.num_web_layers = num_web_layers

		self.top_flange_thickness = num_flange_layers_top*paper_thickness
		self.bottom_flange_thickness = num_flange_layers_bottom*paper_thickness
		self.web_thickness = num_web_layers*paper_thickness

	def get_I_A(self):#Get the I for the A section! (It's still pi shaped)
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist


		flange_a = flange_width*top_flange_thickness
		web_a = 2*web_thickness*(height-top_flange_thickness)
		flange_Y = height - top_flange_thickness/2
		web_Y = (height - top_flange_thickness)/2
		flange_aY = flange_a*flange_Y
		web_aY = web_a * web_Y

		AY = flange_aY + web_aY
		yb = AY/(flange_a + web_a)

		y_flange = flange_Y-yb;
		y_web = web_Y-yb;

		flange_ay2 = flange_a*(y_flange**2)
		web_ay2 = web_a*(y_web**2)

		web_I = ((2*web_thickness)*((height-top_flange_thickness)**3))/12
		flange_I = (flange_width*(top_flange_thickness**3))/12

		sum_ay2 = flange_ay2 + web_ay2
		sum_I = web_I + flange_I

		return sum_ay2+sum_I

	def get_I_B(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		bottom_flange_thickness = self.bottom_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist



		top_flange_a = flange_width*top_flange_thickness
		web_a = 2*web_thickness*(height-top_flange_thickness)
		top_flange_Y = (height - top_flange_thickness/2)+bottom_flange_thickness
		web_Y = ((height - top_flange_thickness)/2)+bottom_flange_thickness
		top_flange_aY = top_flange_a*top_flange_Y
		web_aY = web_a * web_Y

		bottom_flange_a = flange_width*bottom_flange_thickness
		bottom_flange_Y = bottom_flange_thickness/2
		bottom_flange_aY = bottom_flange_a*bottom_flange_Y


		AY = top_flange_aY + web_aY + bottom_flange_aY
		yb = AY/(top_flange_a + web_a + bottom_flange_a)

		y_top_flange = top_flange_Y-yb;
		y_web = web_Y-yb;
		y_bottom_flange = bottom_flange_Y-yb;

		top_flange_ay2 = top_flange_a*(y_top_flange**2)
		web_ay2 = web_a*(y_web**2)
		bottom_flange_ay2 = bottom_flange_a*(y_bottom_flange**2)

		web_I = ((2*web_thickness)*((height-top_flange_thickness)**3))/12
		top_flange_I = (flange_width*(top_flange_thickness**3))/12
		bottom_flange_I = (flange_width*(bottom_flange_thickness**3))/12

		sum_ay2 = top_flange_ay2 + web_ay2 + bottom_flange_ay2
		sum_I = web_I + top_flange_I + bottom_flange_I

		return sum_ay2+sum_I


	def get_centroid_A(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		flange_a = flange_width*top_flange_thickness
		web_a = 2*web_thickness*(height-top_flange_thickness)
		flange_Y = height - top_flange_thickness/2
		web_Y = (height - top_flange_thickness)/2
		flange_aY = flange_a*flange_Y
		web_aY = web_a * web_Y

		AY = flange_aY + web_aY
		yb = AY/(flange_a + web_a)

		return yb

	def get_centroid_B(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		bottom_flange_thickness = self.bottom_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist



		top_flange_a = flange_width*top_flange_thickness
		web_a = 2*web_thickness*(height-top_flange_thickness)
		top_flange_Y = (height - top_flange_thickness/2)+bottom_flange_thickness
		web_Y = ((height - top_flange_thickness)/2)+bottom_flange_thickness
		top_flange_aY = top_flange_a*top_flange_Y
		web_aY = web_a * web_Y

		bottom_flange_a = flange_width*bottom_flange_thickness
		bottom_flange_Y = bottom_flange_thickness/2
		bottom_flange_aY = bottom_flange_a*bottom_flange_Y


		AY = top_flange_aY + web_aY + bottom_flange_aY
		yb = AY/(top_flange_a + web_a + bottom_flange_a)

		return yb

	def get_midspan_deflection(self, P): #P is the point load applied to the middle of the bridge
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		flange_thickness = self.flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I()

		M = (P/2) * (length/2)
		phi_max = M/(E*I)
		dac = 0.5*phi_max*(length/2)*(2/3)*(length/2)
		return dac

	#TODO: Check against group's calculations...
	def get_max_P_flexural_A(self): #Calculates the maximum P the bridge can handle without flexural failure.
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I_A()
		y = self.get_centroid_A()

		#Calculating P for Tension failure
		'''
		M = (max_tensile*I)/Y
		M = 0.08305P -> P = M/0.08305
		'''


		M = (max_tensile*I)/y #maximum moment that this section can endure...
		P = M/83.05
		P1 = P

		#Calculating P for Compressive failure
		M = (max_compressive*I)/(height-y)
		P = M/83.05
		P2 = P

		return [P1, P2]

	def get_max_P_flexural_B(self): #Calculates the maximum P the bridge can handle without flexural failure.
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		flange_thickness = self.top_flange_thickness
		bottom_flange_thickness = self.bottom_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I_B()
		y = self.get_centroid_B()

		#Calculating P for Tension failure
		'''
		M = (max_tensile*I)/Y
		M = 0.08305P -> P = M/0.08305

		'''


		M = (max_tensile*I)/(height+bottom_flange_thickness-y) #maximum moment that this section can endure...
		P = M/94.94
		P1 = P

		#Calculating P for Compressive failure
		M = (max_compressive*I)/(y)
		P = M/94.94
		P2 = P

		return [P1, P2]

	def get_max_P_shear_A(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I_A()
		y = self.get_centroid_A()

		Q = web_thickness*2*y*(y/2)

		P = (6.622516556*max_shear*I*(2*web_thickness))/Q

		return P;

	def get_max_P_shear_B(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		bottom_flange_thickness = self.bottom_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I_B()
		y = self.get_centroid_B()

		# Q = web_thickness*2*y*(y/2)
		area_webs = (y-bottom_flange_thickness)*web_thickness*2
		bottom_area = bottom_flange_thickness*flange_width

		y_bottom = bottom_flange_thickness/2
		y_web = ((y-bottom_flange_thickness)/2)+bottom_flange_thickness

		centroid2 = ((y_bottom*bottom_area+y_web*area_webs)/(area_webs+bottom_area))

		Q = (y-centroid2)*(area_webs+bottom_area) #TODO: double check this calculation

		P = (2*max_shear*I*(2*web_thickness))/Q

		return P;

	def get_buckling_failure_A(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I_A()
		y = self.get_centroid_A()
		Q = web_thickness*2*y*(y/2)

		#pt. 1: Compressive flange
		sig_comp_crit = ((4*(pi**2)*E)/(12*(1-mu**2)))*((flange_thickness/web_dist)**2);
		P = ((I*4*(pi**2)*E)/(83.05*y*12*(1-mu**2)))*((flange_thickness/web_dist)**2);
		P1 = P

		#pt. 2: Flexural compression @ top of web
		sig_comp_crit = ((6*(pi**2)*E)/(12*(1-mu**2)))*(( web_thickness /(height-y-flange_thickness))**2);
		P = ((I*6*(pi**2)*E)/(83.05*y*12*(1-mu**2)))*(( web_thickness /(height-y-flange_thickness))**2);
		P2 = P

		#pt. 3: shear buckling the top of the web
		Tau_crit = ((5*(pi**2)*E)/(12*(1-(mu**2))))*(((web_thickness/(height-flange_thickness))**2) + ((web_thickness/dia_dist)**2))
		V = (Tau_crit*I*(2*web_thickness))/Q
		P = V/0.151
		P3 = P
		# print("Tau_crit = ",Tau_crit)
		# print("22x10^3,",Q)

		#pt. 4: Compressive buckling at the edge of the thing.
		t = flange_thickness
		b = (flange_width - web_dist)/2
		# sig_comp_crit = ((0.425*(pi**2)*E)/(12*(1-mu**2)))*((flange_thickness/((flange_width-web_dist)/2) ))**2);
		P = ((I*0.425*(pi**2)*E)/(83.05*y*12*(1-mu**2)))*((t/b)**2);
		P4 = P

		return [P1, P2, P3, P4]

	def get_buckling_failure_B(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		bottom_flange_thickness = self.bottom_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I_B()
		y = self.get_centroid_B()

		# Q = web_thickness*2*y*(y/2)
		area_webs = (y-bottom_flange_thickness)*web_thickness*2
		bottom_area = bottom_flange_thickness*flange_width

		y_bottom = bottom_flange_thickness/2
		y_web = ((y-bottom_flange_thickness)/2)+bottom_flange_thickness

		centroid2 = ((y_bottom*bottom_area+y_web*area_webs)/(area_webs+bottom_area))

		Q = (y-centroid2)*(area_webs+bottom_area) #TODO: double check this calculation

		#pt. 1: Compressive flange (BOTTOM flange)
		sig_comp_crit = ((4*(pi**2)*E)/(12*(1-mu**2)))*((bottom_flange_thickness/web_dist)**2);
		P = ((I*4*(pi**2)*E)/(94.94*y*12*(1-mu**2)))*((bottom_flange_thickness/web_dist)**2);
		P1 = P

		#pt. 2: Flexural compression @ BOTTOM of web
		sig_comp_crit = ((6*(pi**2)*E)/(12*(1-mu**2)))*(( web_thickness /(y-bottom_flange_thickness))**2);
		P = ((I*6*(pi**2)*E)/(94.94*y*12*(1-mu**2)))*(( web_thickness /(y-bottom_flange_thickness))**2);
		P2 = P

		#pt. 3: shear buckling the top of the web
		Tau_crit = ((5*(pi**2)*E)/(12*(1-(mu**2))))*(((web_thickness/(height-top_flange_thickness))**2) + ((web_thickness/dia_dist)**2))
		V = (Tau_crit*I*(2*web_thickness))/Q
		P = V/0.5
		P3 = P

		#pt. 4: Compressive buckling at the edge of the thing.
		t = bottom_flange_thickness
		b = (flange_width - web_dist)/2
		# sig_comp_crit = ((0.425*(pi**2)*E)/(12*(1-mu**2)))*((flange_thickness/((flange_width-web_dist)/2) ))**2);
		P = ((I*0.425*(pi**2)*E)/(94.94*y*12*(1-mu**2)))*((t/b)**2);
		P4 = P

		return [P1, P2, P3, P4]

	def get_amount_paper(self):
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		num_flange_layers_top = self.num_flange_layers_top
		num_flange_layers_bottom = self.num_flange_layers_bottom
		num_web_layers = self.num_web_layers

		paper_used = (flange_width*length*num_flange_layers_top)+(num_web_layers*2*(height-top_flange_thickness)*length)
		paper_used += num_flange_layers_bottom*flange_width*(mandatory_length-split_point)
		num_diaphragms = (length/dia_dist)+5
		area_dia = num_diaphragms*(height-top_flange_thickness)*web_dist;
		paper_used += area_dia

		return paper_used


	def is_valid(self):
		# return True
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		num_flange_layers_top = self.num_flange_layers_top
		num_flange_layers_bottom = self.num_flange_layers_bottom
		num_web_layers = self.num_web_layers

		paper_used = self.get_amount_paper()

		if total_matboard < paper_used:
			# print("not enough board!")
			return False
		if flange_width < web_dist:
			# print("spatial wack")
			return False
		if flange_width < 100:
			return False
		# if web_dist < 50:
			# return False

		return True

	def get_max_load_A(self):
		return min(self.get_max_P_shear_A(), min(self.get_max_P_flexural_A()), min(self.get_buckling_failure_A()))
	def get_max_load_B(self):
		return min(self.get_max_P_shear_B(), min(self.get_max_P_flexural_B()), min(self.get_buckling_failure_B()))
	def get_max_load(self):
		return min(self.get_max_load_A(), self.get_max_load_B())

	def report(self):
		print("|===========================================================|")
		print("=== DIMENSIONS OF BRIDGE ===")
		print("Height: ",self.height)
		print("Length: ",self.length)
		print("Flange Width: ",self.flange_width)
		print("Web Distance: ",self.web_dist)
		print("Diaphragm Distance: ",self.dia_dist)
		print("Top Flange Thickness: ",self.top_flange_thickness)
		print("Bottom Flange Thickness ",self.bottom_flange_thickness)
		print("Web Thickness: ",self.web_thickness)
		print("\n=== WEIGHT BEARING OF THE BRIDGE: SECTION A ===")
		print("I value: ",self.get_I_A())
		print("Centroid: ",self.get_centroid_A())
		print("Maximum Shear: ",self.get_max_P_shear_A())
		print("Maximum Compression: ",self.get_max_P_flexural_A()[1])
		print("Maximum Tension: ",self.get_max_P_flexural_A()[0])
		print("Maximum for Compressive Flange Buckling: ",self.get_buckling_failure_A()[0])
		print("Maximum for Flexural Compression @Top of Web: ",self.get_buckling_failure_A()[1])
		print("Maximum for Shear Buckling @ Top of Web: ",self.get_buckling_failure_A()[2])
		print("Maximum for Shear Buckling @ Side of Top Flange: ",self.get_buckling_failure_A()[3])
		print("\n=== WEIGHT BEARING OF THE BRIDGE: SECTION B ===")
		print("I value: ",self.get_I_B())
		print("Centroid: ",self.get_centroid_B())
		print("Maximum Shear: ",self.get_max_P_shear_B())
		print("Maximum Compression: ",self.get_max_P_flexural_B()[1])
		print("Maximum Tension: ",self.get_max_P_flexural_B()[0])
		print("Maximum for Compressive Flange Buckling: ",self.get_buckling_failure_B()[0])
		print("Maximum for Flexural Compression @Top of Web: ",self.get_buckling_failure_B()[1])
		print("Maximum for Shear Buckling @ Top of Web: ",self.get_buckling_failure_B()[2])
		print("Maximum for Shear Buckling @ Side of Top Flange: ",self.get_buckling_failure_B()[3])
		print("---------")
		print("\033[1mTotal load bearing ability: ",self.get_max_load(),"\033[0m")
		print("Amount of paper used: ",self.get_amount_paper(),"/",total_matboard)
		print("Validity of evolved design: ",self.is_valid())
		print("|===========================================================|")


def mutate(b, alpha):#b is a bridge, we're returning another mutated bridge

	#paper_thickness, height, length, flange_width, num_flange_layers_top, num_flange_layers_bottom, num_web_layers, web_dist, dia_dist):

	b2 = Bridge(1.27, 102.54, mandatory_length, 105, 2, 2, 1, 55, 91.43)
	b2.height = b.height+(random.random()-0.5)*alpha
	b2.flange_width = b.flange_width+(random.random()-0.5)*alpha
	b2.web_dist = b.web_dist+(random.random()-0.5)*alpha
	b2.dia_dist = b.dia_dist+(random.random()-0.5)*alpha

	b2.length = b.length

	good_to_go = False

	while not good_to_go:

		r1 = random.random()

		if(r1<(1/3)):
			if(random.random()>0.5):
				b2.num_flange_layers_top += 1
			else:
				b2.num_flange_layers_top -= 1

		if(random.random()<(1/3)):
			if(random.random()>0.5):
				b2.num_flange_layers_bottom += 1
			else:
				b2.num_flange_layers_bottom -= 1

		r1 = random.random()
		
		if(r1<(1/3)):
			if(random.random()>0.5):
				b2.num_web_layers += 1
			else:
				b2.num_web_layers -= 1

		if b2.num_flange_layers_top	== 0:
			b2.num_flange_layers_top = 1
		if b2.num_web_layers == 0:
			b2.num_web_layers = 1
		if b2.num_flange_layers_bottom == 0:
			b2.num_flange_layers_bottom = 1

		b2.flange_thickness_top = b2.num_flange_layers_top*b2.paper_thickness
		b2.flange_thickness_bottom = b2.num_flange_layers_bottom*b2.paper_thickness
		b2.web_thickness = b2.num_web_layers*b2.paper_thickness
		good_to_go = True

	return b2

def ascend(b, num_steps):
	# Goal: Get all the failure mechanisms to be as similar as possible.
	b1 = b

	cnt = 0

	maxloads = [];

	for cnt in tqdm(range(num_steps)):


		if not b1.is_valid():
			print("YOUR INITIAL DESIGN WAS NOT VALID!")

		maxloads.append(mb1);

	return [b1, maxloads];

def bridge_write(b, succ_num, g_num):
	file = open("evolve_outputs/"+str(succ_num)+".txt", 'w')
	

	str_out = ""
	str_out += str(b.paper_thickness) + "\n"
	str_out += str(b.height) + "\n"
	str_out += str(b.flange_width) + "\n"
	str_out += str(b.web_dist) + "\n"
	str_out += str(b.length) + "\n"
	str_out += str(b.dia_dist) + "\n"
	str_out += str(b.num_flange_layers_top) + "\n"
	str_out += str(b.num_flange_layers_bottom) + "\n"
	str_out += str(b.num_web_layers) + "\n"
	str_out += str(b.top_flange_thickness) + "\n"
	str_out += str(b.bottom_flange_thickness) + "\n"
	str_out += str(b.web_thickness) + "\n"
	str_out += str(g_num) + "\n"
	str_out += str(b.get_max_load())

	file.write(str_out)


def evolve(b, num_generations, alpha):
	b1 = b

	b2 = mutate(b1, alpha)

	cnt = 0

	maxloads = [];

	success_num = 0 #version number of this bridge (not including failed generations)
	generation_num = 0

	for cnt in tqdm(range(num_generations)):
	# for cnt in range(num_generations):
		mb1 = b1.get_max_load()
		mb2 = b2.get_max_load()

		if(b2.is_valid() and mb1 < mb2):
			b1 = copy.deepcopy(b2)
			# b1 = b2
			b2 = mutate(b2, alpha)
			bridge_write(b1, success_num, generation_num)
			success_num += 1


		else:
			b2 = mutate(b1, alpha)

		if not b1.is_valid():
			print("YOUR INITIAL DESIGN WAS NOT VALID!")

		maxloads.append(mb1);

		generation_num += 1

	return [b1, maxloads];