# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

import ezdxf
import matplotlib.pyplot as plt
#plt.ion()
import numpy


#def read_lines(filename, color = None ,layer = None):
def read_lines(filename, color = None):
    '''
    Reads a dxf file searching for line objects,

    :param filename: the file path of the source dxf
    :type filename: string
    :param color: optional.  if included, this function filters for objects of only this color
    :rtype: List of lines consisting of two two-coordinate tuples each.
    '''
    dwg = ezdxf.readfile(filename)
    modelspace = dwg.modelspace()
    lines = []
    for e in modelspace:
        if e.dxftype() == 'LINE':
    #        red is code 1, gets added to hinge lines
            if color is None:
                lines.append([(e.dxf.start[0],e.dxf.start[1]),(e.dxf.end[0],e.dxf.end[1])])
            else:
                if e.get_dxf_attrib('color')==color:
                    lines.append([(e.dxf.start[0],e.dxf.start[1]),(e.dxf.end[0],e.dxf.end[1])])
    return lines

#def read_lwpolylines(filename,color = None,layer = None):
def read_lwpolylines(filename,color = None):
    '''
    Reads a dxf file searching for lwpolyline objects,

    :param filename: the file path of the source dxf
    :type filename: string
    :param color: optional.  if included, this function filters for objects of only this color
    :rtype: List of lines consisting of two two-coordinate tuples each.
    '''
    dwg = ezdxf.readfile(filename)
    modelspace = dwg.modelspace()
    lines = []
    for e in modelspace:
        if e.dxftype() == 'LWPOLYLINE':
            if color is None:
                lines.append(list(e.get_points()))
            else:
                if e.get_dxf_attrib('color')==color:
                    lines.append(list(e.get_points()))
    return lines

def approx_lwpoly(lines):
    lines = numpy.array(lines)
    circles = []
    for ii in range(len(lines)):
        if lines[ii,4]!=0:
            circles.append(calc_circle(lines[ii,:2],lines[ii+1,:2],lines[ii,4]))
    return circles
            
def calc_circle(p1,p2,f):
#    sign = lambda x: x and (1,-1)[x<0]
    import math
    from foldable_robotics.layer import Layer
    
    
    v = p2 - p1
    
    l = ((v*v)**.5).sum()
    n =v/l
    R = numpy.array([[0,-1],[1,0]])
    n_p = R.dot(n)
    
    p3 = p1+v/2+n_p*-f*l/2
#    d = ((abs(f)*l))
#    r = d/2
#    c = (r**2 - (l/2)**2)**.5
#    center = p1+v/2+c*n_p*sign(f)*-1
    import shapely.geometry as sg
    ls = Layer(sg.LineString([tuple(p1),tuple(p3),tuple(p2)])).buffer(.1)
    
    
    x1_0 = p1[0]
    x1_1 = p1[1]
    x2_0 = p2[0]
    x2_1 = p2[1]
    x3_0 = p3[0]
    x3_1 = p3[1]
    p = numpy.array([ x1_0/2 + x3_0/2 + (x1_1 - x3_1)*((x1_0 - x2_0)*(x2_0 - x3_0) + (x1_1 - x2_1)*(x2_1 - x3_1))/(2*((x1_0 - x3_0)*(x2_1 - x3_1) - (x1_1 - x3_1)*(x2_0 - x3_0))),x1_1/2 + x3_1/2 + (-x1_0 + x3_0)*((x1_0 - x2_0)*(x2_0 - x3_0) + (x1_1 - x2_1)*(x2_1 - x3_1))/(2*((x1_0 - x3_0)*(x2_1 - x3_1) - (x1_1 - x3_1)*(x2_0 - x3_0)))])
#    cp = Layer(sg.Point(*p))
    v = p-p1
    r = (v.dot(v))**.5
#    c = cp.buffer(r)
    
    v1=(p1-p)
    v2=(p2-p)
    t1 = math.atan2(v1[1],v1[0])
    t2 = math.atan2(v2[1],v2[0])
    
    if f<0:
        if t2>t1:
            t2 = t2 - math.pi
    
    n = 20
    t = numpy.r_[t1:t2:n*1j]
    points = r*numpy.c_[numpy.cos(t),numpy.sin(t)] +p
    ls = Layer(sg.LineString(points))
    
    return ls



def list_attrib(filename,attrib):
    '''
    list the attributes of all the items in the dxf.  use a string like 'color' or 'layer'
    '''
    
    dwg = ezdxf.readfile(filename)
    modelspace = dwg.modelspace()
    attrib_list =[]
    for item in modelspace:
        try:
            attrib_list.append(item.get_dxf_attrib(attrib))
        except AttributeError:
            attrib_list.append(None)
    return attrib_list

def get_types(filename,model_type):    
    dwg = ezdxf.readfile(filename)
    modelspace = dwg.modelspace()
    items = list(modelspace.query(model_type))
    return items

if __name__=='__main__':
    #Here goes the file name of the dxf.
    filename ='C:/Users/daukes/code/foldable_robotics/python/tests/test2.DXF'
    dwg = ezdxf.readfile(filename)
    modelspace = dwg.modelspace()
    hinge_lines = read_lines(filename)
    exteriors = read_lwpolylines(filename)
    
    
    #turn lists into arrays
    hinge_lines = numpy.array(hinge_lines)
    
    for item in hinge_lines:
        plt.plot(item[:,0],item[:,1],'r--')
    
    for item in exteriors:
        item = numpy.array(item)
        plt.plot(item[:,0],item[:,1],'k-', linewidth = 3)
        
    plt.axis('equal')
#    print(list_attrib(filename,'closed'))
    items = get_types(filename,'LWPOLYLINE')
    c  = approx_lwpoly(exteriors[0])
    for item in c:
        item.plot()
    