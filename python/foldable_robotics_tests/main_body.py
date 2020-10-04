#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:46:15 2020

@author: danaukes
"""


from foldable_robotics.layer import Layer
from foldable_robotics.laminate import Laminate
import shapely.geometry as sg

import support_tab
import motor_housing
import foldable_robotics.plotter_support as ps
import serial
import time

motor_l = .72
motor_w = .9
motor_th = .5
body_h = 3.5
body_w = 2
body_th = .5
staple_gap = .5

body_total_w = 2*(body_w)+2*body_th
body_layer = Layer(sg.box(0,0,body_total_w,body_h))
body_layer = body_layer.translate(-body_total_w /2,-body_h/2)
        

slit = sg.LineString([(0,-body_h/2),(0,body_h/2)])
slit = Layer(slit)

slits = slit.translate(body_w/2,0) | slit.translate((body_w/2+body_th),0)

slits |= slits.rotate(180)

# joint = sg.LineString([(l,0),(l,w)])
joint = Layer()
# slits= Layer(sg.LineString([(0,0),(1,0)]),sg.LineString([(.25,.5),(.75,.5)]))

# cut = sg.LineString([(0,0),(l+h,0)])
cuts = Layer()
# cuts = cut | cut.translate(0,w)

lam = Laminate(body_layer,Layer(),slits,cuts,joint)

housing_lines = []
housing_lines.append(((body_w/2,.5),(body_w/2,1)))
housing_lines.append(((body_w/2,.5),(body_w/2,1)))

st_lines = []
st_lines.append((((body_w+body_th),1.5),((body_w+body_th),.5)))
st_lines.append(((-(body_w+body_th),.5),(-(body_w+body_th),1.5)))
st_lines.append((((body_w+body_th),-.5),((body_w+body_th),-1.5)))
st_lines.append(((-(body_w+body_th),-1.5),(-(body_w+body_th),-.5)))
h_lines = []
h_lines.append(((0,1.5),(0,.5)))
h_lines.append(((0,-.5),(0,-1.5)))


for line in st_lines:
    lam|=support_tab.lam.map_line_stretch(*support_tab.place_line,*line)

holes = Laminate(*([Layer()]*len(lam)))
for line in h_lines:
    lam |=support_tab.hole.map_line_stretch(*support_tab.place_line,*line)
# lam -= (holes<<.01)

housing = Laminate(*([Layer()]*len(lam)))
for line in housing_lines:
    housing |=motor_housing.lam.map_line_place(*motor_housing.place_line,*line)

housing |= housing.scale(-1,1)
housing |= housing.scale(1,-1)

lam |=housing

# lam = lam.map_line_scale((0,0),(1,0),(0,0),(2,1))
# lam = Laminate(*lam,Layer(sg.LineString([(.25,0),(.75,0)])))
# hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))

# hole = Laminate(Layer(sg.LineString([(.25,0),(.75,0)])))
# 
# (hole<<.01).plot()



(minx,miny),(maxx,maxy) = lam.bounding_box_coords()
lam = lam.translate(-maxx,-miny)

if __name__=='__main__':
    # lam.plot()
    
    
    s = ps.layer_string(lam[0])
    bs = s.encode()
    print(s)
    
    s2 = ps.layer_string(lam[2])
    bs2 = s2.encode()
    print(s2)
    s3 = ps.layer_string(lam[3])
    bs3 = s3.encode()
    print(s3)
    
    with serial.Serial(port = 'COM3',
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=None,
                        xonxoff=True,
                        rtscts=False,) as ser:
        input('set pressure high:')
        print(ser.name)         # check which port was really used
        ser.write(bs)     # write a string
        ser.write(bs)     # write a string
        ser.write(bs)     # write a string
        time.sleep(1)    
        input('set pressure low:')
        ser.write(bs2)     # write a string
        ser.write(bs3)     # write a string
        ser.write(bs3)     # write a string
        ser.write(bs3)     # write a string
        time.sleep(1)    
    
        # ser.close()             # close port
    
    
    
