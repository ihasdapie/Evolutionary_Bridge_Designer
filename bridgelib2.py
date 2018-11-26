'''
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
	- Midspan deflection under 400N
	- Determine P value that will cause 16 MPa tensile stress @max and 6 MPa tensile stress @max (done, needs checking)
	- Determine P value that will cause 4 MPa shear stress ()
	- Check P for plate buckling (top flange, flex of web, shear of web)
	- 
'''

import math as math
import random as random
from tqdm import tqdm
###CIV VARIABLES###
E = 4000
max_tensile = 30
max_compressive = 6
max_shear = 4
mu = 0.2 #poisson's ratio
max_shear_cement = 2
pi = math.pi

mandatory_length = 1280

split_point = 798 #from right to left: go from cross section A to B 

total_matboard = 813*1016 #826008

###ML VARIABLES###
alpha = 10


# Bridge of type discussed in class
class Bridge:
	def __init__(self, paper_thickness, height, length, flange_width, num_flange_layers_top, num_flange_layers_bottom, num_web_layers, web_dist, dia_dist):
		self.paper_thickness = paper_thickness
		self.height = height #webs + top flange (doesn't include bottom flange)
		self.flange_width = flange_width
		self.web_dist = web_dist
		self.length = length
		self.dia_dist = dia_dist
		self.num_flange_layers_top = num_flange_layers_top
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
		print("Maximum P for tensile is:",P1)

		#Calculating P for Compressive failure
		M = (max_compressive*I)/(height-y)
		P = M/83.05
		P2 = P
		print("Maximum P for compressive is:",P2)

		return min(P1, P2)

	def get_max_P_flexural_B(self): #Calculates the maximum P the bridge can handle without flexural failure.
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		flange_thickness = self.top_flange_thickness
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


		M = (max_tensile*I)/y #maximum moment that this section can endure...
		P = M/94.94
		P1 = P
		print("Maximum P for tensile is:",P1)

		#Calculating P for Compressive failure
		M = (max_compressive*I)/(height-y)
		P = M/94.94
		P2 = P
		print("Maximum P for compressive is:",P2)

		return min(P1, P2)

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
		flange_thickness = self.flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		I = self.get_I()
		y = self.get_centroid()
		Q = web_thickness*2*y*(y/2)

		#pt. 1: Compressive flange
		sig_comp_crit = ((4*(pi**2)*E)/(12*(1-mu**2)))*((flange_thickness/web_dist)**2);
		P = ((2*I*4*(pi**2)*E)/(0.5*length*y*12*(1-mu**2)))*((flange_thickness/web_dist)**2);
		P1 = P

		#pt. 2: Flexural compression @ top of web
		sig_comp_crit = ((6*(pi**2)*E)/(12*(1-mu**2)))*(( web_thickness /(height-y-flange_thickness))**2);
		P = ((2*I*6*(pi**2)*E)/(0.5*length*y*12*(1-mu**2)))*(( web_thickness /(height-y-flange_thickness))**2);
		P2 = P

		#pt. 3: shear buckling the top of the web
		Tau_crit = ((5*(pi**2)*E)/(12*(1-(mu**2))))*(((web_thickness/(height-flange_thickness))**2) + ((web_thickness/dia_dist)**2))
		V = (Tau_crit*I*(2*web_thickness))/Q
		P = V*2
		P3 = P
		# print("Tau_crit = ",Tau_crit)
		# print("22x10^3,",Q)

		return min(P1, P2, P3)

	def is_valid(self):
		# return True
		height = self.height
		flange_width = self.flange_width
		web_dist = self.web_dist
		top_flange_thickness = self.top_flange_thickness
		web_thickness = self.web_thickness
		length = self.length
		dia_dist = self.dia_dist

		num_flange_layers = self.num_flange_layers
		num_web_layers = self.num_web_layers

		if total_matboard < (flange_width*length*num_flange_layers)+(num_web_layers*2*(height-flange_thickness)*length):
			# print("not enough board!")
			return False
		if flange_width < web_dist:
			# print("spatial wack")
			return False
		if flange_width < 100:
			return False

		return True

	def get_max_load_A(self):
		return min(self.get_max_P_shear(), self.get_max_P_flexural(), self.get_buckling_failure())

	def report(self):
		print("|====================================|")
		print("Height:",self.height)
		print("Flange Width: ",self.flange_width)
		print("Web Distance: ",self.web_dist)
		print("Diaphragm Distance: ",self.dia_dist)
		print("Flange Thickness: ",self.flange_thickness)
		print("Web Thickness: ",self.web_thickness)
		print("---------")
		print("Total load bearing ability: ",self.get_max_load())
		print("|====================================|")


def mutate(b):#b is a bridge, we're returning another mutated bridge
	b2 = Bridge(1.27, 110, 950, 180, 3, 1, 75, 400)
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
				b2.num_flange_layers += 1
			else:
				b2.num_flange_layers -= 1

		r1 = random.random()
		
		if(r1<(1/3)):
			if(random.random()>0.5):
				b2.num_web_layers += 1
			else:
				b2.num_web_layers -= 1

		if b2.num_flange_layers	== 0:
			b2.num_flange_layers = 1
		if b2.num_web_layers == 0:
			b2.num_web_layers = 1

		b2.flange_thickness = b2.num_flange_layers*b2.paper_thickness
		b2.web_thickness = b2.num_web_layers*b2.paper_thickness

		good_to_go = b2.is_valid()

	return b2



b1 = Bridge(1.27, 180, mandatory_length, 110, 3, 3, 1, 75, 450)
print("Max P for shearing the B section:",b1.get_max_P_shear_A())


