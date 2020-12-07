import bridgelib_2020
# import bridgelib_withsupport
import copy

#paper_thickness, height, length, flange_width, num_flange_layers, num_web_layers,
# web_dist, diaphragm_dist:

b = bridgelib_2020.Bridge(1.27, 100, 980, 120, 2, 1, 80, 300)


import random
def mutate(b, alpha):#b is a bridge, we're returning another mutated bridge
        b2 = b.copy()
        b2.height = b.height+(random.random()-0.5)*alpha
        # b2.flange_width = b.flange_width+(random.random()-0.5)*alpha
        b2.web_dist = b.web_dist+(random.random()-0.5)*alpha
        b2.diaphragm_dist = b.diaphragm_dist+(random.random()-0.5)*alpha
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


def evolve(b, num_generations, alpha):
    b1 = b.copy()
    b2 = mutate(b1, alpha)
    cnt = 0
    success_num = 0 #version number of this bridge (not including failed generations)
    generation_num = 0
    ret = {}
    for cnt in range(num_generations):
        # for cnt in range(num_generations):
        mb1 = b1.get_max_load()
        mb2 = b2.get_max_load()

        if(b2.is_valid() and mb1 < mb2):
            b1 = copy.deepcopy(b2)
            b2 = mutate(b2, alpha)
            # bridge_write(b1, success_num, generation_num)
            success_num += 1
        else:
            b2 = mutate(b1, alpha)
        if not b1.is_valid():
            print("YOUR INITIAL DESIGN WAS NOT VALID!")             
            generation_num += 1
        ret[mb1] = b1.copy()

    return ret





