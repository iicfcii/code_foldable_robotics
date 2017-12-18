# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
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

a = Layer(sg.box(-1,-1,1,1))
f = Layer(sg.Point(1,0).buffer(1))
h = Layer(sg.Polygon([(0,0),(1,0),(1,1)])).translate(0,-3)
b = a<<.2
c = ((a<<.4) - (a>>.25)) | h
d = ((f<<.4) - (f>>.25)) | h
e = f<<.2

adhesive = [False,True,False,True,False]

device = Laminate(a,b,c,d,e,f)

keepout_laser1 = foldable_robotics.manufacturing.keepout_laser(device)
keepout_mill_up1 = foldable_robotics.manufacturing.keepout_mill_up(device)
keepout_mill_down1 = foldable_robotics.manufacturing.keepout_mill_down(device)
keepout_mill_flip1= foldable_robotics.manufacturing.keepout_mill_flip(device)

sheet = foldable_robotics.manufacturing.bounding_box(device<<1)

not_removable_both1 = foldable_robotics.manufacturing.not_removable_both(device)
not_removable_up1 = foldable_robotics.manufacturing.not_removable_up(device,adhesive)
not_removable_down1 = foldable_robotics.manufacturing.not_removable_down(device,adhesive)

scrap_removable_both = sheet-not_removable_both1
scrap_removable_up = sheet - not_removable_up1
scrap_removable_down = sheet - not_removable_down1
scrap_removable = scrap_removable_both|scrap_removable_up|scrap_removable_down

support1=foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_laser,.25,.1)
support2=foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_mill_up,.25,.1)
support3=foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_mill_down,.25,.1)
support4=foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_mill_flip,.25,.1)

worst_case_supported_design = support1|device|(scrap_removable_both-(device<<.25))
best_case_supported_design = support4|device|(scrap_removable-(device<<.25))

#---------------------

device.plot(new=True)
plt.title('device')

#---------------------

fig = plt.figure()

ax=fig.add_subplot(2,2,1)
ax.set_title('Laser Keepout')
keepout_laser1.plot()

ax=fig.add_subplot(2,2,2)
ax.set_title('Mill(from above) keepout')
keepout_mill_up1.plot()

ax=fig.add_subplot(2,2,3)
ax.set_title('Mill(from below) keepout')
keepout_mill_down1.plot()

ax=fig.add_subplot(2,2,4)
ax.set_title('Mill(with flipping) keepout')
keepout_mill_flip1.plot()

#---------------------

sheet.plot(new=True)
plt.title('bounding box of buffered device')

fig = plt.figure()
ax1=fig.add_axes([0.1,.1,.2,.8])
ax1.set_title('Not Removable Both')
not_removable_both1.plot()


ax2=fig.add_axes([0.4,.1,.2,.8])
ax2.set_title('Not Removable Up')
not_removable_up1.plot()

ax3=fig.add_axes([0.7,.1,.2,.8])
ax3.set_title('Not Removable Down')
not_removable_down1.plot()

#---------------------

fig = plt.figure()
ax1=fig.add_axes([0.1,.6,.2,.3])
scrap_removable_both.plot()
ax1.set_title('Removable Both')

ax2=fig.add_axes([0.4,.6,.2,.3])
scrap_removable_up.plot()
ax2.set_title('Removable up')

ax3=fig.add_axes([0.7,.6,.2,.3])
scrap_removable_down.plot()
ax3.set_title('Removable down')

ax4=fig.add_axes([0.1,.1,.8,.3])
scrap_removable.plot()
ax4.set_title('All removable scrap')

#---------------------

fig = plt.figure()
ax=fig.add_subplot(2,2,1)
ax.set_title('Support_laser')
support1.plot()
ax=fig.add_subplot(2,2,2)
ax.set_title('support(mill above)')
support2.plot()
ax=fig.add_subplot(2,2,3)
ax.set_title('support(mill below)')
support3.plot()
ax=fig.add_subplot(2,2,4)
ax.set_title('support(mill&flip)')
support4.plot()

#---------------------

fig = plt.figure()
ax=fig.add_subplot(1,2,1)
ax.set_title('Supported device design(worst case)')
worst_case_supported_design.plot()
ax=fig.add_subplot(1,2,2)
ax.set_title('Supported device design(best case)')
best_case_supported_design.plot()

best_case_supported_design.plot_layers()
worst_case_supported_design.plot_layers()