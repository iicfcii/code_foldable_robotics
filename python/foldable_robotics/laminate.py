# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from .class_algebra import ClassAlgebra

class WrongNumLayers(Exception):
    pass

class IterableLaminate(object):

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.list[index]

        elif isinstance(index, slice):
            return self.list[index]

    def __setitem__(self, index, v):
        if isinstance(index, int):
            self.list[index] = v
            
        elif isinstance(index, slice):
            self.list[index] = v

    def __iter__(self):
        for item in self.list:
            yield item

    def __len__(self):
        return len(self.list)

class Laminate(IterableLaminate,ClassAlgebra):
    def __init__(self, *layers):
        self.layers = layers
        self.id = id(self)

    def copy(self,identical = True):
        new = type(self)(*[layer.copy(identical) for layer in self.layers])
        if identical:        
            new.id = self.id
        return new

    def plot(self):
        for geom in self.layers:
            geom.plot()
    
    @property
    def list(self):
        return self.layers

    def binary_operation(self,function_name,other,*args,**kwargs):
        if len(self.layers)!=len(other.layers):
            raise(WrongNumLayers())
        else:
            layers = []
            for layer1,layer2 in zip(self.layers,other.layers):
                function = getattr(layer1,function_name)
                layers.append(function(layer2))
            return type(self)(*layers)

    def unary_operation(self,function_name,*args,**kwargs):
            layers = []
            for layer1 in self.layers:
                function = getattr(layer1,function_name)
                layers.append(function(*args,**kwargs))
            return type(self)(*layers)
            
    def union(self,other):
        return self.binary_operation('union',other)

    def difference(self,other):
        return self.binary_operation('difference',other)

    def symmetric_difference(self,other):
        return self.binary_operation('symmetric_difference',other)

    def intersection(self,other):
        return self.binary_operation('intersection',other)
    
    def dilate(self,value,resolution = None):
        return self.unary_operation('dilate',value,resolution=resolution)

    def erode(self,value,resolution = None):
        return self.unary_operation('erode',value,resolution=resolution)

    def translate(self,dx,dy):
        return self.unary_operation('translate',dx,dy)
        
    def rotate(self,angle,about=None):
        return self.unary_operation('rotate',angle,about=about)

#    @list.setter
#    def list(self,v):
#        self.layers = v