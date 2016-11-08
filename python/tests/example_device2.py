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

import foldable_robotics.manufacturing

def lines_to_shapely(hinge_lines):
    hinge_line = sg.LineString([(0,0),(1,0)])
    hinge_layer = Layer(hinge_line)
    all_hinges1 = [hinge_layer.map_line_stretch((0,0),(1,0),*toline) for toline in hinge_lines]
    return all_hinges1

def calc_hole(hinge_lines,width,resolution = 2):
    all_hinges1= lines_to_shapely(hinge_lines)
    all_hinges11 = [item.dilate(w/2,resolution = resolution) for item,w in zip(all_hinges1,width)]
    
    plt.figure()
    all_hinges3 = []
    for ii,hinge in enumerate(all_hinges11):
        all_hinges2 = Layer()
        for item in all_hinges11[:ii]+all_hinges11[ii+1:]:
            all_hinges2|=item
        all_hinges3.append(hinge&all_hinges2)
    
    all_hinges4 = Layer()
    for item in all_hinges3:
        all_hinges4|=item
    all_hinges4.plot(new=True)
    
    holes = Laminate(*([all_hinges4]*5))
    
    trimmed_lines = [item-all_hinges4 for item in all_hinges1]
    all_hinges = [list(item.geoms[0].coords) for item in trimmed_lines]
    return holes,all_hinges

#create a layer named box
box = Layer(sg.box(0,0,1,1))

#initialize layer01 as box, and union with the same box translated several times
layer01 = box
layer01 = layer01 | box.translate(1,-1)
layer01 = layer01.translate(.5,0)
layer01 = layer01 | layer01.affine_transform([-1,0,0,1,0,0])
layer01.plot()

layer34 = layer01.affine_transform([1,0,0,-1,0,0])

hinge = Laminate(layer01,layer01,Layer(),layer34,layer34)
hinge_hole = Layer(sg.box(-.5,-1,.5,1))
hinge |= Laminate(hinge_hole,hinge_hole,hinge_hole,hinge_hole,hinge_hole)
hinge = hinge.affine_transform([1,0,0,.05,0,0])

plt.figure()
hinge.plot()

body = Layer(sg.box(-1,-1,1,1))
body = Laminate(body,body,body,body,body)
plt.figure()
body.plot()

#create a layer with nothing in it
empty_layer = Layer()

#create a list of lines represented as tuples of two points as a reference for transforming my hinge:
hinge_lines = []
hinge_lines.append(((0,0),(1,1)))
hinge_lines.append(((0,0),(0,1)))
hinge_lines.append(((0,0),(1,0)))
hinge_lines.append(((0,0),(-1,0)))
hinge_lines.append(((0,0),(0,-1)))
hinge_lines.append(((0,0),(-1,-1)))
hinge_lines.append(((0,0),(-1,1)))
hinge_lines.append(((0,0),(1,-1)))

holes,hinge_lines2 = calc_hole(hinge_lines,[.1]*len(hinge_lines))

#create an empty laminate
all_hinges = Laminate(empty_layer,empty_layer,empty_layer,empty_layer,empty_layer)
for to_point0,to_point1 in hinge_lines:
    #transform my hinge so that it is stretched, rotated, and translated to the desired hinge line.
    new_hinge = hinge.map_line_stretch((-2.5,0),(2.5,0),to_point0,to_point1)
    #add the new_hinge to the laminate of all hinges with a union
    all_hinges = all_hinges | new_hinge 
    #this is the shorthand version:
    #all_hinges |= new_hinge 
    
plt.figure()
all_hinges.plot()

#create a layer composed of a single Linestring
#cut = Layer(sg.LineString([(0,0),(1,0)])) 
cut = Layer(sg.Point((0,0))) 
cut= cut<<.2
#make a laminate of 5 of the same layers
all_cuts = Laminate(cut,cut,cut,cut,cut) 

empty = Layer()
layer_numbers = Laminate(empty,empty,empty,empty,empty)
jig = Laminate(empty,empty,empty,empty,empty)

#holes,hinge_lines = calc_hole(hinge_lines,[.1]*len(hinge_lines))
device = body-all_hinges-(holes<<.01)
device.plot(new=True)

asdf  = lines_to_shapely(hinge_lines)
asdf2 = Layer()
for item in asdf:
    asdf2 |= item
asdf2 <<=.001
asdf3 = Laminate(asdf2,asdf2,asdf2,asdf2,asdf2)
separated_device = device - asdf3
separated_device.plot(True)

connected = foldable_robotics.manufacturing.find_connected(separated_device,[False,True,False,True,False])
for item in connected:
    item.plot(new=True)