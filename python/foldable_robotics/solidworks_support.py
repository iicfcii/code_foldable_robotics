# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:23:36 2019

@author: daukes
"""

import yaml
import numpy
import matplotlib.pyplot as plt
import os
import shapely.geometry as sg
from foldable_robotics.layer import Layer
import foldable_robotics.layer

class obj(object):
    pass

def objectify(var):
    if isinstance(var,dict):
        new_var = obj()
        for key,value in var.items():
            setattr(new_var,key,objectify(value))
        return new_var
    elif isinstance(var,list):
        new_var = [objectify(item) for item in var]
        return new_var
    else: 
        return var    
        
class Component(object):
    pass

class Face(object):
    pass

def create_loops(filename):
#    plt.figure()
    with open(filename) as f:
        data1 = yaml.load(f)
    data = objectify(data1)
    global_transform = numpy.array(data.transform)
    components = []
    for component in data.components:
        new_component = Component()
        local_transform = numpy.array(component.transform)
        T = local_transform.dot(global_transform)
        faces = []
        for face in component.faces:
            new_face = Face()
            loops = []
            for loop in face.loops:
                loop = numpy.array(loop)
                loop_a = numpy.hstack([loop,numpy.ones((len(loop),1))])
                loop_t = loop_a.dot(T)
                loop_out = loop_t[:,:2].tolist()
                loops.append(loop_out)
#                plt.fill(loop_t[:,0],loop_t[:,1])
            new_face.loops = loops
            faces.append(new_face)
        new_component.faces = faces
        components.append(new_component)
    return components

def component_to_layer(component):
    faces = []
    for face in component.faces:
        loops = []
        for loop in face.loops:
            loops.append(Layer(sg.Polygon(loop)))
        if not not loops:
            face_new = loops.pop(0)            
            for item in loops:
                face_new^=item
            faces.append(face_new)
    if not not faces:
        component_new = faces.pop(0)
        for item in faces:
            component_new|=item
        return component_new
            
def get_joints(component_layers,roundvalue):

#    tolerance = 10**(-roundvalue)

#    lines = []
    
    component_segments = []
    for layer in component_layers:
        segments = []
        for geom in layer.geoms:
            segments.extend(foldable_robotics.layer.get_segments(geom))
        component_segments.append(segments)
    return component_segments
#        p = geom.exteriorpoints()
#        lines.extend(zip(p, p[1:] + p[:1]))
#        for interior in geom.interiorpoints():
#            lines.extend(zip(interior, interior[1:] + interior[:1]))
#
#    l3 = popupcad.algorithms.points.distance_of_lines(lines, [0, 0])
#    l4 = popupcad.algorithms.points.distance_of_lines(lines, [10 * tolerance, 0])
#    l5 = popupcad.algorithms.points.distance_of_lines(lines, [10 * tolerance, 10 * tolerance])
#    l6 = popupcad.algorithms.points.distance_of_lines(lines, [0, 10 * tolerance])
#    l7 = popupcad.algorithms.points.distance_of_lines(lines, [10 * tolerance, 20 * tolerance])
#    
#    m = numpy.c_[l3, l4, l5, l6, l7]
#    m = m.round(roundvalue)
#    m2 = [tuple(items) for items in m.tolist()]
#    m3 = list(set(m2))
##    jj = numpy.searchsorted(m3,m2)
#    index_to_unique = [m3.index(item) for item in m2]
#    indeces_to_orig = [[] for item in m3]
#    [indeces_to_orig[item].append(ii) for ii, item in enumerate(index_to_unique)]
#
#    newsegments = []
#    for segments in indeces_to_orig:
#        if len(segments) > 1:
#            a = [lines[ii] for ii in segments]
#            vertices = []
#            [vertices.extend(item) for item in a[1:]]
#            ordered_vertices = popupcad.algorithms.points.order_vertices(vertices,a[0],tolerance=tolerance)
#            segs = list(zip(ordered_vertices[:-1], ordered_vertices[1:]))
#            midpoints = popupcad.algorithms.points.segment_midpoints(segs)
#            count = [0 for item in midpoints]
#            for ii in segments:
#                for jj, point in enumerate(midpoints):
#                    if popupcad.algorithms.points.point_within_line(point,lines[ii],tolerance=tolerance):
#                        count[jj] += 1
#            newsegments.extend([seg for count_ii, seg in zip(count, segs) if count_ii > 1])
#
#    generic_lines = [GenericLine([ShapeVertex(v1), ShapeVertex(v2)], []) for v1, v2 in newsegments]
#    generic_lines = [item for item in generic_lines if len(item.get_exterior()) == 2]
#    return generic_lines
            
            
                
if __name__=='__main__':
    user_path = os.path.abspath(os.path.expanduser('~'))
    filename = os.path.normpath(os.path.join(user_path,'class_foldable_robotics/cad/spherical_example/input.yaml'))
    components = create_loops(filename)
    layers = [component_to_layer(item) for item in components]
    layer2 = Layer()
    for item in layers:
        layer2 |= item>>1e-3
    layer2.plot(new=True)
    