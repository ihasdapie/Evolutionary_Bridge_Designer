#######################
# CIV102 Final Matboard Bridge Project
# 
# Based on https://github.com/amanb2000/Evolutionary_Bridge_Designer
# 
# Copyright © 2020 | CIV102 Group 83 | Brian Chen, Jacky Liao, Leon Qian, Simon Wang
# 
#######################

import copy
import math as math
import random as random
import json
from tqdm import tqdm


########## Define constants here ############
E = 4000 # mpa
max_tensile = 30 #mpa
max_compressive = 6 #mpa
max_shear = 4 #mpa
mu = 0.2 #poisson's ratio
max_shear_cement = 2 #mpa
pi = math.pi
mandatory_length = 980 #mm
total_matboard = 814*1016 #827024 mm^2
load_d = 280 # mm
############################################
inter_load_d = mandatory_length - (2*load_d)

class Bridge:
    """
    A simply supported bridge subjected to symmetric loading


                      <-----------span---------------->

                       load_d P/2            P/2 load_d 
                      <------> ↓            ↓ <------> 
    --------------    ---------------|-----------------
    |  flange    |    |___|_____|____|____|____|____|__|
    --------------                   |    <---->               
     | |      | |     ^              |  diaphragm_dist ^
     | |      | |    /  \            |                /  \ 
     | |      | |                    |
     | |      | | <--- webs        CL (centerline)
     ---      ---
    
    """
    def __init__(self, paper_thickness, height, length, flange_width, num_flange_layers, num_web_layers, web_dist, diaphragm_dist):
        self.paper_thickness = paper_thickness
        self.height = height
        self.flange_width = flange_width
        self.web_dist = web_dist
        self.length = length
        self.diaphragm_dist = diaphragm_dist
        self.num_flange_layers = num_flange_layers
        self.num_web_layers = num_web_layers
        self.flange_thickness = num_flange_layers*paper_thickness
        self.web_thickness = num_web_layers*paper_thickness
        self.y_bar = self.get_centroid() # centroidal axis, ȳ
        self.I = self.get_I()

    @classmethod
    def loadBridge(cls, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(data['paper_thickness'], data['height'], data['length'],
                   data['flange_width'], data['num_flange_layers'], data['num_web_layers'],
                   data['web_dist'], data['diaphragm_dist'])

    def get_centroid(self, show_calc=False):
        "returns centroidal axis , y_bar relative to bottom of pi-beam"

    # get areas 
        flange_a = self.flange_width*self.flange_thickness
        web_a = 2*self.web_thickness*(self.height-self.flange_thickness)

    # get distance from the centroid of the areas to the bottom of beam
        flange_Y = self.height - (self.flange_thickness/2)
        web_Y = (self.height - self.flange_thickness)/2

    # get weighted sum of distances
        flange_aY = flange_a*flange_Y
        web_aY = web_a * web_Y
        sum_aY = flange_aY + web_aY

    # divide weighted sum with sum to get centroidal axis
        yb = sum_aY/(flange_a + web_a)

        if show_calc:
            print("({fy}*{fa} + {wy} + {wy}*{wa})/{s}".format(fy=flange_Y, fa=flange_a, wy=web_Y, wa = web_a, s = (flange_a + web_a)))
        return yb

       

    def get_I(self, show_calc=False):
        "sum(A*d) about centroidal axis:"
        # get areas 
        flange_a = self.flange_width*self.flange_thickness
        web_a = 2*self.web_thickness*(self.height-self.flange_thickness)

        # get distance from the centroid of the areas to the bottom of beam
        flange_Y = self.height - (self.flange_thickness/2)
        web_Y = (self.height - self.flange_thickness)/2
        

        # I = (bh^3)/12
        web_I = ((2*self.web_thickness)*((self.height-self.flange_thickness)**3))/12
        flange_I = (self.flange_width*(self.flange_thickness**3))/12

        # parallel axis thereom, I = I_o + Ad^2
        flange_aY = flange_a*flange_Y
        web_aY = web_a * web_Y

        sum_aY = flange_aY + web_aY
        yb = sum_aY/(flange_a + web_a)

        y_flange = flange_Y-yb;
        y_web = web_Y-yb;

        flange_ay2 = flange_a*(y_flange**2)
        web_ay2 = web_a*(y_web**2)

        sum_ay2 = flange_ay2 + web_ay2
        sum_I = web_I + flange_I

        if show_calc:
            print("I_web = {I_o} + {A}*{d}^2".format(I_o=web_I, A = web_a, y = web_Y))
            print("I_flange = {I_o} + {A}*{d}^2".format(I_o=flange_I, A = flange_a, y = flange_Y))
            print("I_total = ", sum_ay2 + sum_I)
        return sum_ay2+sum_I
    

    def get_midspan_deflection(self, P, show_calc=False): #P is the point loads applied at load_d from edge
        # using moment area thereom #2

        # A------------------------B (curvature diagram)
        # \                       /
        #  \                     /
        #   ---------M----------- (Φ_max)

        global load_d, inter_load_d
        M = (P/2) * self.load_d # units N*mm
        # get curvature per unit length, rad/mm Φ=M/EI
        phi_max = M/(E*self.I)

        # get deflection using M.A.T #2
        # if the bridge is supported at points A & B and the midpoint is M,
        dist_1 = (2/3)*load_d # distance from area midpoints to A
        dist_2 = load_d + inter_load_d/4

        A1 = (0.5*phi_max*load_d)*dist_1 # triangular portion
        A2 = (phi_max*inter_load_d) * dist_2 
        
        d_ma = (A1*dist_1) + (A2*dist_2) # triangular portion
        if show_calc:
            print("{a1}*{d1} + {a2}*{d2} = {ans}".format(a1=A1, d1=dist_1, a2=A2, d2=dist_2, ans=d_ma))
        return d_ma

    def get_max_P_flexural(self, show_calc=False): #Calculates the maximum P the bridge can handle without flexural failure.
        # σ = (M*y_bar)/I
        # M = load_d * (P/2)
        # P = (2Iσ)/(y_bar*load_d)
        global max_tensile, max_compressive, load_d 
        

        P_tension_max = (2*self.I*max_tensile)/(self.y_bar*load_d)
        P_compressive_max = (2*self.I*max_compressive)/(self.y_bar*load_d)

        if show_calc:
            print("Maximum P for tensile is:", P_tension_max)
            print("Maximum P for compression is: ", P_compressive_max)
            # haven't bothered to write the str format yet
        return min(P_compressive_max, P_tension_max)

    def get_max_P_shear(self, show_calc=False):
        # max shear is found at the centroidal axis which
        # for all reasonable bridges is located across the webs
        # τ = VQ/Ib
        # τ is given, find V (shear force = P/2) max
        global max_shear
        # using Q as calculated from the "legs"
        # Q = sum(A*d)
        Q = (self.y_bar/2)*(self.web_thickness*self.y_bar)
        b = self.web_thickness*2
        V_max = (2*(self.I*b*max_shear))/Q

        if show_calc:
            print(Q, b) # might be nice to prettyprint this ...

        return V_max

    def get_buckling_failure(self, show_calc=False):
        global E, mu, load_d, pi

        Q = (self.y_bar/2)*(self.web_thickness*self.y_bar)
        #pt. 1: Compressive flange failure
        # looking at the flange between the webs
        # σ_crit  = ((4π^2E)/(12(1-u^2))) (t/b)^2
        sig_comp_flange_crit = ((4*(pi**2)*E)/(12*(1-mu**2)))*((self.flange_thickness/self.web_dist)**2)
        
        #TODO: I'm not 100% on what y should be. I think height bc that's the very top? 
        #  σ = My/I = sig_comp_flange_crit
        p_comp_flange_crit = (sig_comp_flange_crit*2*self.I)/(self.height * load_d)

        # P = ((2*I*4*(pi**2)*E)/(0.5*length*y*12*(1-mu**2)))*((flange_thickness/web_dist)**2); 
        # ^ that is how it was done previously...note how they did not divide? 
        #  σ = My/I = sig_comp_flange_crit, P = (2Iσ)/(height*load*d) -- M = load_d*(P/2)
        
        #pt. 2: the little flange bits that extend outside of the webs 
        sig_comp_flange_flap_crit = ((0.425*(pi**2)*E)/(12*(1-mu**2)))*((self.flange_thickness/(self.flange_width-self.web_dist))**2)
        p_comp_flange_flap_crit = (sig_comp_flange_flap_crit*2*self.I)/(self.height * load_d)


        #pt 3: The web between y_bar and top 
        sig_comp_web_crit = ((6*(pi**2)*E)/(12*(1-mu**2)))*((self.web_thickness/(self.height-self.y_bar-self.flange_thickness))**2)
        # we only want the max -> use y = y_top = height - flange_thickness
        p_comp_web_crit = (sig_comp_flange_flap_crit*2*self.I)/((self.height-self.flange_thickness) * load_d)

        #pt. 4: diaphragms 
        tau_crit_diaphragm = ((5*(pi**2)*E)/(12*(1-(mu**2))))
        tau_crit_diaphragm *= ((self.web_thickness/(self.height-self.flange_thickness))**2 + (self.web_thickness/self.diaphragm_dist))
        # τ = VQ/Ib
        p_diaphram_crit = 2*((tau_crit_diaphragm*self.I*self.web_thickness)/Q)

        return min(p_diaphram_crit, p_comp_flange_crit, p_comp_flange_flap_crit, p_comp_web_crit)

    def is_valid(self, show_calc=False):
        global total_matboard
        if total_matboard < (self.flange_width*self.length*self.num_flange_layers)+(self.num_web_layers*2*(self.height-self.flange_thickness)*self.length) + (self.flange_width*(self.height-self.flange_thickness)*(self.length//self.diaphragm_dist)):
                print("not enough board!")
                return False
        if self.flange_width < self.web_dist:
                print("spatial wack")
                return False
        return True

    def get_max_load(self, show_calc=False):
        return min(self.get_max_P_shear(), self.get_max_P_flexural(), self.get_buckling_failure())

    def report(self, show_calc=False):
        print("|====================================|")
        print("I: ", self.I)
        print("Y_bar", self.y_bar)
        print("Height:",self.height)
        print("Flange Width: ",self.flange_width)
        print("Web Distance: ",self.web_dist)
        print("Diaphragm Distance: ",self.diaphragm_dist)
        print("Flange Thickness: ",self.flange_thickness)
        print("Web Thickness: ",self.web_thickness)
        print("---------")
        print("Total load bearing ability: ",self.get_max_load())
        print("is valid?: ", self.is_valid())
        print("|====================================|")
        
    def copy(self):
        nb = Bridge(self.paper_thickness, self.height, self.length, self.flange_width, self.num_flange_layers, self.num_web_layers, self.web_dist, self.diaphragm_dist)
        return nb

    def toJson(self):
        A = {}
        A['paper_thickness'] = self.paper_thickness
        A['height'] = self.height
        A['flange_width'] = self.flange_width
        A['web_dist'] = self.web_dist
        A['length'] = self.length
        A['diaphragm_dist'] = self.diaphragm_dist
        A['num_flange_layers'] = self.num_flange_layers
        A['num_web_layers'] = self.num_web_layers
        A['flange_thickness'] = self.flange_thickness
        A['web_thickness'] = self.web_thickness
        A['y_bar'] = self.y_bar
        A['I'] = self.I
        return A
    def write(self, path):
        with open(path, 'w') as f:
            json.dump(self.toJson(), f)
            f.close()
        return 
