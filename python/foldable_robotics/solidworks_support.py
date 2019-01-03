# -*- coding: utf-8 -*-
"""
Created on Thu Jan  3 14:23:36 2019

@author: daukes
"""

import yaml
import numpy
import matplotlib.pyplot as plt

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
plt.figure()

def create_loops(filename):
    with open(filename) as f:
        data1 = yaml.load(f)
    data = objectify(data1)
    global_transform = numpy.array(data.transform)
    components = []
    for item in data.components:
        component = Component()
        local_transform = numpy.array(item.transform)
        T = local_transform.dot(global_transform)
        faces = []
        for item in item.faces:
            face = Face()
            loops = []
            for loop in item.loops:
                loop = numpy.array(loop)
                loop_a = numpy.hstack([loop,numpy.ones((len(loop),1))])
                loop_t = loop_a.dot(T)
                loops.append(loop_t)
                plt.fill(loop_t[:,0],loop_t[:,1])
            face.loops = loops
            faces.append(face)
        component.faces = faces
        components.append(component)
                
if __name__=='__main__':
    components = create_loops('input.yaml')