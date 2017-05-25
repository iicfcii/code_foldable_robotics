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
from idealab_tools.geometry.tetrahedron import Tetrahedron
from idealab_tools.geometry.triangle import Triangle
import foldable_robotics.manufacturing


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

holes,hinge_lines2 = foldable_robotics.manufacturing.calc_hole(hinge_lines,[.1]*len(hinge_lines))

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

asdf  = foldable_robotics.manufacturing.lines_to_shapely(hinge_lines)
asdf2 = Layer()
for item in asdf:
    asdf2 |= item
asdf2 <<=.001
asdf3 = Laminate(asdf2,asdf2,asdf2,asdf2,asdf2)
separated_device = device - asdf3
separated_device.plot(True)

joint_props = {}
for item in hinge_lines2:
    joint_props[tuple(item)] = (1e1,1e0,0,-180,180,.025)

connected = foldable_robotics.manufacturing.find_connected(separated_device,[False,True,False,True,False])
connected_export = [item.export_dict() for item in connected]
asdf  = foldable_robotics.manufacturing.lines_to_shapely(hinge_lines2)
connection = []
for line,coords in zip(asdf,hinge_lines2):
    line<<=.002
#    print('line')
    plt.figure()
    line.plot()
    a=[]
    for item1,item2 in zip(connected,connected_export):
        item11 = foldable_robotics.manufacturing.unary_union(item1)
        if len((item11&line).geoms)!=0:
#            print(item1)
            item11.plot()
            a.append(item1.id)
    connection.append((coords,a))

thickness = [.01]*5
density = [1]*5

foldable_robotics.manufacturing.save_joint_def('test.yaml',connected_export,connection,[connected_export[0]['id']],joint_props,thickness,density)

#asdf2 = Layer()
#for item in asdf:
#    asdf2 |= item

#for item in connected:
#    item.plot(new=True)
#    m,v,(x,y)=mass_properties(item,[.1]*5,[1]*5)
#    plt.plot(x,y,'ro')
#    plt.text(x,y,'asdf')

