# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 20:40:50 2016

@author: danb0b
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


a = Layer(sg.box(-2,-1,2,1))
b = Layer(sg.Point(0,0).buffer(1.5))
c1 = Layer(sg.box(-.25,-.25,.25,.25))
c = c1 | c1.translate(-2,0)| c1.translate(2,0)

device = Laminate(a,b,c,c)

support1 = foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_laser,.2,.1)

sheet = foldable_robotics.manufacturing.bounding_box(device<<2)
scrap = sheet - (foldable_robotics.manufacturing.not_removable_both(device))
scrap = scrap - (device<<.2)

supported_design = scrap|support1|device

first_pass = sheet-(foldable_robotics.manufacturing.keepout_laser(supported_design) - supported_design)
first_pass.plot

final_cut = foldable_robotics.manufacturing.keepout_laser(device)
final_cut = (final_cut<<.05)-(final_cut)

removed = first_pass-final_cut


device.plot(True)
scrap.plot(True)
support1.plot(True)
(support1|scrap).plot(True)
supported_design.plot(True)
removed.plot(True)

support_width = .2
support_gap = .1
hole_buffer = .01

custom_support_line = Layer(sg.LineString([(-3,0),(3,0)]))
custom_support_line2 = Layer(sg.LineString([(0,2),(0,-2)]))
custom_support_line = Laminate(Layer(),Layer(),custom_support_line,custom_support_line2)

modified_device,custom_support,custom_cut = foldable_robotics.manufacturing.modify_device(device,custom_support_line,.1,.2,.01)    
modified_device.plot(True)
#
supported_design2 = (modified_device | support1|custom_support|scrap) 
supported_design2.plot(True)

first_pass2 = sheet-(foldable_robotics.manufacturing.keepout_laser(supported_design2) - supported_design2)
final_cut2 = foldable_robotics.manufacturing.keepout_laser(modified_device)
final_cut2 = ((final_cut2<<.05)-(final_cut2)) | custom_cut
removed2 = first_pass2-final_cut2
removed2.plot(True)
