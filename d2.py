# For square shape support
# dimension in mm
# P returned in kN
# plug in numbers at the bottom
# calculate(b,L,t)

import math

def area(b,t):
    ans = b*b - (b-2*t)*(b-2*t)
    return ans

def Second_momentI(b, t):

    ans = b*(b**3)/12 - ((b-2*t)*(b-2*t)**3)/12

    return ans

def check_1(A):
    P = 6*A
    return "The maximum P the bridage can take on before compressing is:"+  str(P) + " kN" + "\n"


def check_2(I, L):

    buckingP = (math.pi*(4000)*I)/(L**2)

    return "The maximum P for buckling is "+ str(buckingP) + " kN" + "\n"

def check_3(t,b,A):

    stress = 4*(math.pi**2)*(4000)/(12*(1-0.2**2))*(t/b)**2
    P = stress*A

    return "The maximum P for plate buckling is "+ str(P) + " kN" + "\n"

def calculate(b,L,t):
    I = Second_momentI(b,t)
    A = float(area(b,t))

    ans = "base and height = " + str(b) + "\n" + "mm"
    ans += "length = " + str(L) + "\n" + "mm"
    ans += "thickness = " + str(t) + "\n" + "mm"
    ans += check_1(A) + check_2(I,L) + check_3(t,b,A)

    return ans

if __name__ == "__main__":
    print(calculate(100,600,1.27))

### Extra
    # if P < buckingP:
    #     return ("success" + str(P) + "is lesser than buckingP:" + str(bucklingP))
    # if P > buckingP:
    #     return ("fail" + "P:" + str(P) + "is more than buckingP:" + str(bucklingP))

    # print(check_1(550))
    # print(check_2())
