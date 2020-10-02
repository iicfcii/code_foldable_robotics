#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:46:15 2020

@author: danaukes
"""


from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import shapely.geometry as sg
# from math import tan,pi
# import foldable_robotics.plotter_support as ps
# import serial
# import time

overlap = .01
motor_th = .5
box = sg.box(0,-overlap,1,.5)
tab = sg.box(.25,.5,.75,.75)

layer = Layer(box,tab)
# layer.plot()

slits= Layer(sg.LineString([(0,0),(1,0)]),sg.LineString([(.25,.5),(.75,.5)]))

place_line = (0,0),(1,0)

lam = Laminate(layer,Layer(),slits,Layer(),Layer())

# lam = Laminate(*lam,Layer(sg.LineString([(.25,0),(.75,0)])))
hole = Laminate(Layer(),Layer(),Layer(),Layer(sg.LineString([(.25,0),(.75,0)])),Layer())

# hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))



if __name__=='__main__':
    (hole<<.01).plot()
    lam.plot()

