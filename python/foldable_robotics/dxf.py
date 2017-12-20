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
def read_lwpolylines(filename,color = None,arc_approx = 0):
    '''
    Reads a dxf file searching for lwpolyline objects, approximating arc elements in an lwpolyline with an n-segement set of lines

    :param filename: the file path of the source dxf
    :type filename: string
    :param color: optional.  if included, this function filters for objects of only this color
    :param arc_approx: number of interior points to approximate an arc with
    :type arc_approx: int
    :rtype: List of lines consisting of two two-coordinate tuples each.
    '''
    dwg = ezdxf.readfile(filename)
    modelspace = dwg.modelspace()
    lines = []
    for e in modelspace:
        if e.dxftype() == 'LWPOLYLINE':
            if color is None or e.get_dxf_attrib('color')==color:
                line = numpy.array(list(e.get_points()))
                line_out = []
                for ii in range(len(line)):
                    if line[ii,4]!=0:
                        line_out.extend(calc_circle(line[ii,:2],line[ii+1,:2],line[ii,4],arc_approx))
                    else:
                        line_out.append(line[ii,:2].tolist())
                lines.append(line_out)
    return lines

            
def calc_circle(p1,p2,bulge,arc_approx=0):
    '''
    Approximates an arc betweem two points using a "bulge value".

    :param p1: the starting point.
    :type p1: tuple of floats
    :param p2: the ending point.
    :type p2: tuple of floats
    :param bulge: the bulge value. Positive bulge is right of the segment, negative is left.
    :type bulge: int
    :param arc_approx: number of interior points to approximate an arc with
    :type arc_approx: int
    :rtype: List of two-coordinate tuples.
    '''

    import math
    from foldable_robotics.layer import Layer
    
    
    v = p2 - p1
    
    l = ((v*v)**.5).sum()
    n =v/l
    R = numpy.array([[0,-1],[1,0]])
    n_p = R.dot(n)
    
    p3 = p1+v/2+n_p*-bulge*l/2
    
    x1_0 = p1[0]
    x1_1 = p1[1]
    x2_0 = p2[0]
    x2_1 = p2[1]
    x3_0 = p3[0]
    x3_1 = p3[1]
    p = numpy.array([ x1_0/2 + x3_0/2 + (x1_1 - x3_1)*((x1_0 - x2_0)*(x2_0 - x3_0) + (x1_1 - x2_1)*(x2_1 - x3_1))/(2*((x1_0 - x3_0)*(x2_1 - x3_1) - (x1_1 - x3_1)*(x2_0 - x3_0))),x1_1/2 + x3_1/2 + (-x1_0 + x3_0)*((x1_0 - x2_0)*(x2_0 - x3_0) + (x1_1 - x2_1)*(x2_1 - x3_1))/(2*((x1_0 - x3_0)*(x2_1 - x3_1) - (x1_1 - x3_1)*(x2_0 - x3_0)))])

    v = p-p1
    r = (v.dot(v))**.5
    
    v1=(p1-p)
    v2=(p2-p)
    t1 = math.atan2(v1[1],v1[0])
    t2 = math.atan2(v2[1],v2[0])
    
    if bulge<0:
        if t2>t1:
            t2 = t2 - math.pi
    
    t = numpy.r_[t1:t2:(arc_approx+2)*1j]
    points = r*numpy.c_[numpy.cos(t),numpy.sin(t)] +p
    
    return [p1]+points[1:-1].tolist()

def list_attrib(filename,attrib):
    '''
    list the attributes of all the items in the dxf.  use a string like 'color' or 'layer'

    :param filename: path to the dxf.
    :type filename: string
    :param attrib: attribute you wish to search.
    :type attrib: string
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
    '''
    return all of the dxf items of type "type"

    :param filename: path to the dxf.
    :type filename: string
    :param model_type: model type you are looking for.  ex: 'LWPOLYLINE'
    :type model_type: string
    '''
    
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
    exteriors = read_lwpolylines(filename,arc_approx=10)
    
    
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
#    c  = approx_lwpoly(exteriors[0])
#    for item in c:
#        item.plot()
    