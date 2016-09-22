# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 09:55:46 2016

@author: daukes
"""

#import modules from shapely and matplotlib
import shapely.geometry as sg
import matplotlib.pyplot as plt

#import classes from my local modules
from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer

#create a layer named box
box = Layer(sg.box(0,0,1,1))

#initialize layer01 as box, and union with the same box translated several times
layer01 = box
layer01 = layer01 | box.translate(2,0)
layer01 = layer01 | box.translate(1,-1)
layer01.plot()

layer34 = layer01.affine_transform([1,0,0,-1,0,0])

hinge = Laminate(layer01,layer01,Layer(),layer34,layer34)
hinge = hinge.affine_transform([1,0,0,.25,0,0])

plt.figure()
hinge.plot()

outer = Layer(sg.box(0,0,3,5))
outer = Laminate(outer,outer,outer,outer,outer)
plt.figure()
outer.plot()

#create a layer with nothing in it
empty_layer = Layer()

#create a list of lines represented as tuples of two points as a reference for transforming my hinge:
hinge_lines = []
hinge_lines.append(((0,2),(1,2)))
hinge_lines.append(((0,4),(1,4)))
hinge_lines.append(((1,1),(2,1)))
hinge_lines.append(((1,3),(2,3)))
hinge_lines.append(((2,2),(3,2)))
hinge_lines.append(((2,4),(3,4)))

#create an empty laminate
all_hinges = Laminate(empty_layer,empty_layer,empty_layer,empty_layer,empty_layer)
for to_point0,to_point1 in hinge_lines:
    #transform my hinge so that it is stretched, rotated, and translated to the desired hinge line.
    new_hinge = hinge.map_line_stretch((0,0),(3,0),to_point0,to_point1)
    #add the new_hinge to the laminate of all hinges with a union
    all_hinges = all_hinges | new_hinge 
    #this is the shorthand version:
    #all_hinges |= new_hinge 
    
plt.figure()
all_hinges.plot()

#create a layer composed of a single Linestring
cut = Layer(sg.LineString([(0,0),(1,0)])) 
#make a laminate of 5 of the same layers
cut = Laminate(cut,cut,cut,cut,cut) 

#The first cut will be the outer perimeter minus the negative of the desired hinge geometry
first_cut = outer-all_hinges
first_cut = first_cut.affine_transform([10,0,0,10,0,0])
plt.figure()
first_cut.plot()
first_cut.export_dxf('first_cut')

#create al ist of lines represented as tuples of two points as a reference for transforming my cuts
cut_lines = []
cut_lines.append(((1,1),(1,4)))
cut_lines.append(((2,1),(2,4)))

#create an empty laminate
all_cuts = Laminate(empty_layer,empty_layer,empty_layer,empty_layer,empty_layer)
for to_point0,to_point1 in cut_lines:
    #transform my cuts so that it is stretched, rotated, and translated to the desired hinge line.
    new_cut_line = cut.map_line_stretch((0,0),(1,0),to_point0,to_point1)
    #add the new_cut to the laminate of all_cuts using  a union
    all_cuts = all_cuts | new_cut_line
    #this is the shorthand version
#    all_cuts |= new_cut_line
    
#the second cut, which is cut through all layers, is defined as the outer perimeter minus the cut line, buffered by a small amount(to make a cut area)
second_cut = outer-(all_cuts<<.01)
second_cut= second_cut.affine_transform([10,0,0,10,0,0])
plt.figure()
second_cut[0].plot()
second_cut[0].export_dxf('second_cut')