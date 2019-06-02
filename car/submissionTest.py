#!/usr/bin/python2

import submission
import util
from sympy import *

def test1c():
    epsilon = .1
    eta = .2
    p1 = eta
    p2 = (epsilon*eta**2 + (1-epsilon)*(1-eta)*eta) / (epsilon*eta**2 + 2*(1-epsilon)*(1-eta)*eta + epsilon*(1-eta)**2)
    print(p2)
    x = symbols('x')
    print(solveset((x*eta**2 + (1-x)*(1-eta)*eta) / (x*eta**2 + 2*(1-x)*(1-eta)*eta + x*(1-eta)**2) - eta, x))

if __name__ == '__main__':
    test1c()
