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

a = sg.box(-2,-1,2,1)
b = sg.Point(0,0).buffer(1.5)

device = Laminate(Layer(a),Layer(b))

support = foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_laser,.2,.2)

sheet = foldable_robotics.manufacturing.bounding_box(device<<2)
scrap = sheet - (foldable_robotics.manufacturing.not_removable_both(device))
scrap = scrap - (device<<.2)

supported_design = scrap|support|device

first_pass = sheet-(foldable_robotics.manufacturing.keepout_laser(supported_design) - supported_design)
first_pass.plot

final_cut = foldable_robotics.manufacturing.keepout_laser(device)
final_cut = (final_cut<<.05)-(final_cut)
removed = first_pass-final_cut

device.plot(True)
scrap.plot(True)
support.plot(True)
(support|scrap).plot(True)
supported_design.plot(True)
removed.plot(True)
