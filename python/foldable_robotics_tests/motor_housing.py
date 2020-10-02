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


l = .72
w = .9
h = .5

b = sg.box(0,0,l+h,w)

material = Layer(b)

slit = sg.LineString([(0,0),(0,w)])

slit = Layer(slit)
slits = slit | slit.translate(h,0) | slit.translate(l+h,0)

place_line = [(l,0),(l,w)]
joint = sg.LineString(place_line)
joint = Layer(joint)
# slits= Layer(sg.LineString([(0,0),(1,0)]),sg.LineString([(.25,.5),(.75,.5)]))

cut = sg.LineString([(0,0),(l+h,0)])
cut = Layer(cut)
cuts = cut | cut.translate(0,w)

lam = Laminate(material,Layer(),slits,cuts,joint)

# lam = Laminate(*lam,Layer(sg.LineString([(.25,0),(.75,0)])))
# hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))

# hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))
# 
# (hole<<.01).plot()

if __name__=='__main__':

    lam.plot()

