# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 09:12:33 2016

@author: gurupkar nerwal, Dan Aukes
"""

import ezdxf
import matplotlib.pyplot as plt
plt.ion()
import numpy

#Here goes the file name of the dxf.
dwg = ezdxf.readfile("C:/Users/daukes/Desktop/test/test.dxf")
modelspace = dwg.modelspace()

hinge_lines = []
body_lines = []
other_lines = []
exteriors = []

for e in modelspace:
    if e.dxftype() == 'LINE':
#        red is code 1, gets added to hinge lines
        if e.get_dxf_attrib('color')==1:
            hinge_lines.append([(e.dxf.start[0],e.dxf.start[1]),(e.dxf.end[0],e.dxf.end[1])])
#        white is code 7, gets added to body_lines
        elif e.get_dxf_attrib('color')==7:
            body_lines.append([(e.dxf.start[0],e.dxf.start[1]),(e.dxf.end[0],e.dxf.end[1])])
#        any other color code gets added to other_lines
        else:
            other_lines.append([(e.dxf.start[0],e.dxf.start[1]),(e.dxf.end[0],e.dxf.end[1])])
#    if there is an lwpolyline, it was drawn in to indicate the body perimeter
    if e.dxftype() == 'LWPOLYLINE':
        exteriors.append(list(e.get_points()))

#turn lists into arrays
hinge_lines = numpy.array(hinge_lines)
body_lines= numpy.array(body_lines)
other_lines = numpy.array(other_lines)

for item in hinge_lines:
    plt.plot(item[:,0],item[:,1],'r--')
#for item in body_lines:
#    plt.plot(item[:,0],item[:,1],'b-')
for item in other_lines:
    plt.plot(item[:,0],item[:,1],'-')

for item in exteriors:
#    turn each list of exteriors into array
    item = numpy.array(item)
    plt.plot(item[:,0],item[:,1],'k-', linewidth = 5)
    
plt.axis('equal')