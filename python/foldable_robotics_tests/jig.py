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
import foldable_robotics.general

  
if __name__=='__main__':
    hole = Layer(sg.Point((0,0)))
    hole = hole.dilate(4.85/2,4)
    
    holes = foldable_robotics.general.rectangular_array(hole,10,10,5,5)

    holes.plot()
