# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

#import modules from shapely and matplotlib
import shapely.geometry as sg
import matplotlib.pyplot as plt

#import classes from my local modules
from foldable_robotics.laminate import Laminate
from foldable_robotics.layer import Layer

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

device = body-all_hinges-all_cuts
device.plot(new=True)

support1 = foldable_robotics.manufacturing.support(device,foldable_robotics.manufacturing.keepout_laser,.1,.05)
support1.plot(new=True)

sheet = foldable_robotics.manufacturing.bounding_box(device<<1)
sheet.plot(new=True)

all_scrap = sheet-device

is_adhesive = [False,True,False,True,False]

removable_both_scrap = all_scrap - foldable_robotics.manufacturing.not_removable_both(device)
removable_both_scrap =  removable_both_scrap -(device<<.1)

removable_both_scrap.plot(True)
supported_device = (removable_both_scrap|support1|device)
supported_device.plot(True)
for layer in foldable_robotics.manufacturing.cleanup(supported_device,1e-5,0):
    no_errors = True
    if len(layer.geoms)>=2:
        layer.plot(new=True)
        no_errors = False
        plt.title('error?')
if no_errors:
    print('no errors')
        
first_pass = foldable_robotics.manufacturing.keepout_laser(supported_device) - supported_device
first_pass = sheet-first_pass
first_pass -= layer_numbers
first_pass -= jig
first_pass.plot(True)
first_pass.export_dxf('first_pass')

second_pass = foldable_robotics.manufacturing.keepout_laser(device)
#second_pass = sheet - second_pass
second_pass.plot(True)

#this is what you should acutally cut out.
second_pass_actual = sheet-second_pass
second_pass_actual[0].export_dxf('second_pass')


#this is for separating all the parts and checking the cuts.
second_pass_cut_area = (second_pass<<.01) - second_pass
second_pass_cut_area.plot(True)

check = supported_device-second_pass_cut_area
check.plot(True)

parts = foldable_robotics.manufacturing.find_connected(check,is_adhesive)
tests = []

#test resulting cut out parts to make sure one of them matches the original device
for part in parts:
#    part.plot(True)
    test1 = part^device
    test2 = foldable_robotics.manufacturing.cleanup(test1,1e-5,0)
    test3 = foldable_robotics.manufacturing.zero_test(test2) 
    tests.append(test3)    
if any(tests):
    print('device matches')
    
