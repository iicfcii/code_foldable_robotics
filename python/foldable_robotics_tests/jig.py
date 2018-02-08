# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

import shapely.geometry as sg
import matplotlib.pyplot as plt
from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer

def gen_holes(diameter,spacing,num_duplicates,num_layers=5):
    hole = Layer(sg.Point((0,0)))
    hole = hole.dilate(diameter/2,4)
    hole = Laminate(*([hole]*num_layers))
    
    holes = hole.copy()
    s=spacing/2
    for ii in range(num_duplicates):
        s*=2    
        holes2 = holes.translate(s,0)
        holes2 |= holes.translate(s,s)
        holes2 |= holes.translate(0,s)
        holes |= holes2
    holes = holes.translate(-s+spacing/2,-s+spacing/2)
    return holes
    
if __name__=='__main__':
    holes = gen_holes(4.85,10,4,5)
    holes.plot(True)
