'''
Conditions:
        - Bridge will be the same as in the handout (double t-beam, diaphragms throughout)
        - Given variables:
                - Overall height
                - Top flange width
                - Distance between bottom flanges
                - Thickness of vertical flanges
                - Thickness of top flange
                - Overall length
                - Distance bw diaphragms
What we need to calculate:
        - Centroid location (done)
        - Moment of inertia (done)
        - Midspan deflection under 200N
        - Determine P value that will cause 16 MPa tensile stress @max and 6 MPa tensile stress @max
        - Determine P value that will cause 4 MPa shear stress
        - Check P for plate buckling (top flange, flex of web, shear of web)
        - 
'''
import copy
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

mandatory_length = 980

total_matboard = 814*1016 #827024




# Bridge of type discussed in class
class Bridge:
    def __init__(self, paper_thickness, height, length, flange_width, num_flange_layers, num_web_layers, web_dist, dia_dist):
        self.paper_thickness = paper_thickness
        self.height = height
        self.flange_width = flange_width
        self.web_dist = web_dist
        self.length = length
        self.dia_dist = dia_dist
        self.num_flange_layers = num_flange_layers
        self.num_web_layers = num_web_layers
        self.flange_thickness = num_flange_layers*paper_thickness
        self.web_thickness = num_web_layers*paper_thickness

    def get_I(self):
        height = self.height
        flange_width = self.flange_width
        web_dist = self.web_dist
        flange_thickness = self.flange_thickness
        web_thickness = self.web_thickness
        length = self.length
        dia_dist = self.dia_dist

        flange_a = flange_width*flange_thickness
        web_a = 2*web_thickness*(height-flange_thickness)
        flange_Y = height - flange_thickness/2
        web_Y = (height - flange_thickness)/2
        flange_aY = flange_a*flange_Y
        web_aY = web_a * web_Y

        AY = flange_aY + web_aY
        yb = AY/(flange_a + web_a)

        y_flange = flange_Y-yb;
        y_web = web_Y-yb;

        flange_ay2 = flange_a*(y_flange**2)
        web_ay2 = web_a*(y_web**2)

        web_I = ((2*web_thickness)*((height-flange_thickness)**3))/12
        flange_I = (flange_width*(flange_thickness**3))/12

        sum_ay2 = flange_ay2 + web_ay2
        sum_I = web_I + flange_I

        return sum_ay2+sum_I

    def get_centroid(self):
        height = self.height
        flange_width = self.flange_width
        web_dist = self.web_dist
        flange_thickness = self.flange_thickness
        web_thickness = self.web_thickness
        length = self.length
        dia_dist = self.dia_dist

        flange_a = flange_width*flange_thickness
        web_a = 2*web_thickness*(height-flange_thickness)
        flange_Y = height - flange_thickness/2
        web_Y = (height - flange_thickness)/2
        flange_aY = flange_a*flange_Y
        web_aY = web_a * web_Y

        AY = flange_aY + web_aY
        yb = AY/(flange_a + web_a)
        
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

    def get_max_P_flexural(self): #Calculates the maximum P the bridge can handle without flexural failure.
        height = self.height
        flange_width = self.flange_width
        web_dist = self.web_dist
        flange_thickness = self.flange_thickness
        web_thickness = self.web_thickness
        length = self.length
        dia_dist = self.dia_dist

        I = self.get_I()
        y = self.get_centroid()

        #Calculating P for Tension failure
        M = (max_tensile*I)/y
        P = (4*M)/length
        P1 = P
        print("Maximum P for tensile is:",P1)

        #Calculating P for Compressive failure
        M = (max_compressive*I)/(height-y)
        P = (4*M)/length
        P2 = P
        print("Maximum P for compressive is:",P2)

        return min(P1, P2)

    def get_max_P_shear(self):
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

        P = (2*max_shear*I*(2*web_thickness))/Q

        return P;

    def get_buckling_failure(self):
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
        flange_thickness = self.flange_thickness
        web_thickness = self.web_thickness
        length = self.length
        dia_dist = self.dia_dist

        num_flange_layers = self.num_flange_layers
        num_web_layers = self.num_web_layers

        if total_matboard < (flange_width*length*num_flange_layers)+(num_web_layers*2*(height-flange_thickness)*length) + (self.flange_width*(self.height-self.flange_thickness)*(self.length//self.dia_dist)):
                # print("not enough board!")
                return False
        if flange_width < web_dist:
                # print("spatial wack")
                return False

        return True

    def get_max_load(self):
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
        print("is valid?: ", self.is_valid())
        print("|====================================|")

    def copy(self):
        nb = Bridge(self.paper_thickness, self.height, self.length, self.flange_width, self.num_flange_layers, self.num_web_layers, self.web_dist, self.dia_dist)
        return nb


def mutate(b, alpha):#b is a bridge, we're returning another mutated bridge
        b2 = b.copy()
        b2.height = b.height+(random.random()-0.5)*alpha
        # b2.flange_width = b.flange_width+(random.random()-0.5)*alpha
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

            if b2.num_flange_layers == 0:
                b2.num_flange_layers = 1
            if b2.num_web_layers == 0:
                b2.num_web_layers = 1

            b2.flange_thickness = b2.num_flange_layers*b2.paper_thickness
            b2.web_thickness = b2.num_web_layers*b2.paper_thickness

            good_to_go = b2.is_valid()

        return b2

def bridge_write(b, succ_num, g_num):
    file = open("evolve_outputs_3/"+str(succ_num)+".txt", 'w')
    str_out = ""
    str_out += str(b.paper_thickness) + "\n"
    str_out += str(b.height) + "\n"
    str_out += str(b.flange_width) + "\n"
    str_out += str(b.web_dist) + "\n"
    str_out += str(b.length) + "\n"
    str_out += str(b.dia_dist) + "\n"
    str_out += str(b.num_web_layers) + "\n"
    str_out += str(b.web_thickness) + "\n"
    str_out += str(g_num) + "\n"
    str_out += str(b.get_max_load())

    file.write(str_out)



def evolve(b, num_generations, alpha):
    b1 = b.copy()
    b2 = mutate(b1, alpha)
    cnt = 0
    success_num = 0 #version number of this bridge (not including failed generations)
    generation_num = 0
    ret = {}
    for cnt in tqdm(range(num_generations)):
        # for cnt in range(num_generations):
        mb1 = b1.get_max_load()
        mb2 = b2.get_max_load()

        if(b2.is_valid() and mb1 < mb2):
            b1 = copy.deepcopy(b2)
            b2 = mutate(b2, alpha)
            bridge_write(b1, success_num, generation_num)
            success_num += 1
        else:
            b2 = mutate(b1, alpha)
        if not b1.is_valid():
            print("YOUR INITIAL DESIGN WAS NOT VALID!")             
            generation_num += 1
        ret[mb1] = b1.copy()

    return ret




