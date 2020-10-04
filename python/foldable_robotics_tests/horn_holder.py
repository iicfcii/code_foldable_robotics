#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:59:13 2020

@author: danaukes
"""


from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import shapely.geometry as sg
# from math import tan,pi
# import foldable_robotics.plotter_support as ps
# import serial
# import time
import foldable_robotics.plotter_support as ps
import serial
import time

lw = .75
tab_w = .25
l = 3

tw = (lw*(2+2**.5))
dx = (lw+lw/2)
b = sg.box(0,0,tw,l)
tab = sg.box(0,0,tab_w,l)
tab = Layer(tab)

material = Layer(b)
material |= tab.translate(-tab_w,0)
material |= tab.translate(tw,0)
material = material.translate(-dx,-.75)

# cut = Layer(sg.Point(.1,.33))
# cut <<= .02
cut = Layer(sg.LineString([(0,.45),(.06,.45)]))
cut = (cut << .04)
cut |= cut.scale(-1,1)
cut |= cut.scale(1,-1)

# cut2 = Layer(sg.Point(.2,.075))
# cut2 <<= .02
cut2 = Layer(sg.LineString([(.2,0),(.2,.06)]))
cut2 = (cut2 << .04)
cut2 |= cut2.scale(1,-1)
cut2 |= cut2.scale(-1,1)

material -=cut
hole = Layer(sg.Point(0,0))
hole<<=.125
material -= hole
material -= cut2

# material.plot()

slit = Layer(sg.LineString([(0,0),(0,l)]))
slits = slit.translate(-3*lw/2,0) | slit.translate(-lw/2,0) | slit.translate(lw/2,0) | slit.translate(lw*(.5+(2**.5)),0) 
slits = slits.translate(0,-.75)

lam = Laminate(material,slits)
# lam = la
(minx,miny),(maxx,maxy) = lam.bounding_box_coords()
lam = lam.translate(-minx+.1,0)
lam |= lam.scale(-1,1)
lam = lam.rotate(90)
# slits = slit | slit.translate(h,0) | slit.translate(l+h,0)

# place_line = [(l,0),(l,w)]
# joint = sg.LineString(place_line)
# joint = Layer(joint)
# # slits= Layer(sg.LineString([(0,0),(1,0)]),sg.LineString([(.25,.5),(.75,.5)]))

# cut = sg.LineString([(0,0),(l+h,0)])
# cut = Layer(cut)
# cuts = cut | cut.translate(0,w)

# lam = Laminate(material,Layer(),slits,cuts,joint)

# # lam = Laminate(*lam,Layer(sg.LineString([(.25,0),(.75,0)])))
# # hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))

# # hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))
# # 
# # (hole<<.01).plot()

if __name__=='__main__':

    (minx,miny),(maxx,maxy) = lam.bounding_box_coords()
    lam = lam.translate(-maxx,-miny)
    
    lam.plot()
    
    
    s = ps.layer_string(lam[0])
    bs = s.encode()
    print(s)
    
    s2 = ps.layer_string(lam[1])
    bs2 = s2.encode()
    print(s2)
    # s3 = ps.layer_string(lam[3])
    # bs3 = s3.encode()
    # print(s3)
    
    with serial.Serial(port = 'COM3',
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=None,
                        xonxoff=True,
                        rtscts=False,) as ser:
        input('set pressure high:')
        print(ser.name)         # check which port was really used
        ser.write(bs)     # write a string
        ser.write(bs)     # write a string
        ser.write(bs)     # write a string
        time.sleep(1)    
        input('set pressure low:')
        ser.write(bs2)     # write a string
        # ser.write(bs3)     # write a string
        # ser.write(bs3)     # write a string
        # ser.write(bs3)     # write a string
        time.sleep(1)    
    
        # ser.close()             # close port