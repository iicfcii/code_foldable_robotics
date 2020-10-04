#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:46:15 2020

@author: danaukes
"""


from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import shapely.geometry as sg
from math import tan,pi
import foldable_robotics.plotter_support as ps
import serial
import time


length = 2.5
width = .73
triwidth = .25
topwidth = width+triwidth
theta = 30
tab_h = 1
# sg.MultiLineString()
bottom = sg.box(0,0,width,length)
triside = sg.box(0,0,topwidth,length)

layer1 = Layer(bottom)
trilayer = Layer(triside)
layer1 |= trilayer.translate(width,0)

fold1 = sg.LineString([(0,0),(0,length)])
foldlayer = Layer(fold1)
folds = foldlayer.translate(width,0)
folds |= foldlayer.translate(width+topwidth/2-triwidth,0)
folds |= foldlayer.translate(width+topwidth/2,0)
folds |= foldlayer.translate(width+topwidth/2+triwidth,0)

cutback_y = tan(45*pi/180)*triwidth
cuttri = sg.Polygon([(0,0),(triwidth,0),(0,cutback_y)])
cutlayer = Layer(cuttri)
cutlayer |= cutlayer.scale(-1,1)
cutlayer |= cutlayer.scale(1,-1)
cutlam = cutlayer.to_laminate(2)
cutlam.plot()

# layer2 = Layer(fold1)
# layer2 |= layer2.translate(-width,0)
lam = Laminate(layer1,folds)

lam -= cutlam.translate(width+topwidth/2,0)
lam -= cutlam.translate(width+topwidth/2,length)


joint = Layer(sg.LineString([(0,0),(width+topwidth,0)]))
joints = joint | joint.translate(0,length) |joint.translate(0,2*length)

lam2 = lam.copy()
lam2 |= lam.translate(0,length)
lam2 = Laminate(*lam2,joints)


# lam2 |= lam.translate(0,2*length)
# lam2 |= lam.translate(0,3*length)
# lam2 |= lam.translate(0,4*length)
# lam2 |= lam.scale(-1,1).translate(width,4*length)
lay3 = Layer(sg.box(0,0,width*(2+2**.5),-tab_h))
folds = Layer(sg.LineString([(width,0),(width,-tab_h)]))
folds |= Layer(sg.LineString([(2*width,0),(2*width,-tab_h)]))
lam3 = Laminate(lay3,folds,Layer())
lam3 = lam3.translate(-1*width,0)
lam2 |= lam3|lam3.translate(0,length*2+tab_h)


smallcut = Layer(sg.LineString([(0,0),(topwidth,0)]))
smallcut <<= .01
smallcut_lam = smallcut.to_laminate(len(lam2))
lam2-=smallcut_lam.translate(width,length)
# lam2-=smallcut_lam.translate(width,2*length)
# lam2-=smallcut_lam.translate(width,3*length)
# lam2-=smallcut_lam.translate(width,4*length)


# lam2 = lam2.scale(.5,.5)
lam2 = lam2.rotate(90)
(minx,miny),(maxx,maxy) = lam2.bounding_box_coords()
lam2 = lam2.translate(-maxx,-miny)
# lam2 = lam2.rotate(90)

# lam2.export_dxf('test.dxf')

# path_string = ps.path_string(layer1.get_paths()[0])
# print(path_string)
s = ps.layer_string(lam2[0])
bs = s.encode()
print(s)

s2 = ps.layer_string(lam2[1])
bs2 = s2.encode()
print(s2)
s3 = ps.layer_string(lam2[2])
bs3 = s3.encode()
print(s3)

if __name__=='__main__':
    lam2.plot(new=True)
    # with serial.Serial(port = 'COM3',
    #                     baudrate=9600,
    #                     bytesize=serial.EIGHTBITS,
    #                     parity=serial.PARITY_NONE,
    #                     stopbits=serial.STOPBITS_ONE,
    #                     timeout=None,
    #                     xonxoff=True,
    #                     rtscts=False,) as ser:
    #     input('set pressure high:')
    #     print(ser.name)         # check which port was really used
    #     ser.write(bs)     # write a string
    #     ser.write(bs)     # write a string
    #     ser.write(bs)     # write a string
    #     time.sleep(1)    
    #     input('set pressure low:')
    #     ser.write(bs2)     # write a string
    #     ser.write(bs3)     # write a string
    #     time.sleep(1)    
    
    #     # ser.close()             # close port
    
    
    
