# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 09:03:59 2016

@author: daukes
"""
import os
import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
    mpl.use('Agg')

from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer
import shapely.geometry as sg
import matplotlib.pyplot as plt
plt.ion()

import foldable_robotics.manufacturing

a = Layer(sg.box(0,0,1,1))
b = a.translate(.6,.6)
b1 = a.translate(-.6,-.6)
c = b.translate(.6,.6)
c1 = b1.translate(-.6,-.6)
d = c.translate(1.2,1.2)
d1 = c1.translate(-.6,-.6)

A = Laminate(a,b|b1,c|c1,d|d1)
B = A.copy() | (A.rotate(90).translate(-1.4))
#B.plot_layers()
B.plot(True)

adhesive = [True,False,False,True]

results = foldable_robotics.manufacturing.find_connected(B,adhesive)

for item in results:
    item.plot(True)
    
plt.show()