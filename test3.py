# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:55:46 2016

@author: daukes
"""

from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer
import shapely.geometry as sg
import matplotlib.pyplot as plt

box = Layer(sg.box(0,0,1,1))
layer01 = box
layer01 |= box.translate(2,0)
layer01 |= box.translate(1,-1)
layer01.plot()

layer34 = layer01.affine_transform([1,0,0,-1,0,0])

hinge = Laminate(layer01,layer01,Layer(),layer34,layer34)
hinge = hinge.affine_transform([1,0,0,.25,0,0])

cut = Layer(sg.LineString([(0,0),(1,0)])) 
cut = Laminate(cut,cut,cut,cut,cut) 

plt.figure()
hinge.plot()

outer = Layer(sg.box(0,0,3,5))
outer = Laminate(outer,outer,outer,outer,outer)
plt.figure()
outer.plot()

hinge_lines = []
hinge_lines.append(((0,2),(1,2)))
hinge_lines.append(((0,4),(1,4)))
hinge_lines.append(((1,1),(2,1)))
hinge_lines.append(((1,3),(2,3)))
hinge_lines.append(((2,2),(3,2)))
hinge_lines.append(((2,4),(3,4)))

cut_lines = []
cut_lines.append(((1,1),(1,4)))
cut_lines.append(((2,1),(2,4)))

null_layer = Layer()


base = Laminate(null_layer,null_layer,null_layer,null_layer,null_layer)
for c0,c1 in hinge_lines:
    base|=hinge.map_line_stretch((0,0),(3,0),c0,c1)
    
plt.figure()
base.plot()

first_cut = outer-base
first_cut = first_cut.affine_transform([10,0,0,10,0,0])
plt.figure()
first_cut.plot()
first_cut.export_dxf('first_cut')

base = Laminate(null_layer,null_layer,null_layer,null_layer,null_layer)
for c0,c1 in cut_lines:
    base|=cut.map_line_stretch((0,0),(1,0),c0,c1)

second_cut = outer-(base<<.01)
second_cut= second_cut.affine_transform([10,0,0,10,0,0])
plt.figure()
second_cut[0].plot()
second_cut[0].export_dxf('second_cut.dxf')