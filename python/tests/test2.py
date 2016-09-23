# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 22:19:47 2016

@author: danb0b
"""

#import matplotlib.pyplot as plt
#plt.ion()
from foldable_robotics.shape import Polygon,Polyline,Point
from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate

a = Polygon.make_rect_center(1,.5)
b = a.dilate(.5,4)[0]
c = (b-a)[0]
d = Polygon.make_circle_r((1,0),1)

#plt.figure()
#[item.plot() for item in d|c]

#plt.figure()
#[item.plot() for item in d&c]

#plt.figure()
#[item.plot() for item in d-c]

#plt.figure()
#[item.plot() for item in c-d]

#plt.figure()
#[item.plot() for item in d^c]

a = Layer(d)
b = a.dilate(.2)

A = Laminate(a)
B = Laminate(b)
C = B-A
CC=A.dilate(.2)-A
#plt.figure()
#C.plot()

#plt.figure()
#CC.plot()

