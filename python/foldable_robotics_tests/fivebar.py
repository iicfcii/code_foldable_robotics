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

length = 4
width = 2
triwidth = .5
topwidth = width+triwidth
theta = 30
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



lam = Laminate(*lam,Layer(sg.LineString([(0,0),(width,0)])))
lam2 = lam.copy()
lam2 |= lam.translate(0,length)
lam2 |= lam.translate(0,2*length)
lam2 |= lam.translate(0,3*length)
lam2 |= lam.scale(-1,1).translate(width,4*length)

smallcut = Layer(sg.LineString([(0,0),(topwidth,0)]))
smallcut <<= .01
smallcut_lam = smallcut.to_laminate(len(lam2))
lam2-=smallcut_lam.translate(width,length)
lam2-=smallcut_lam.translate(width,2*length)
lam2-=smallcut_lam.translate(width,3*length)
lam2-=smallcut_lam.translate(width,4*length)

lam2.plot(new=True)

lam2.export_dxf('test.dxf')

# path_string = ps.path_string(layer1.get_paths()[0])
# print(path_string)
s = ps.layer_string(layer1)
print(s)