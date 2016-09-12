# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

from class_algebra import ClassAlgebra
import geometry

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
        import matplotlib.cm
        cm = matplotlib.cm.coolwarm
        l = len(self.layers)        
        for ii,geom in enumerate(self.layers):
            
            geom.plot(color = cm(ii/l))
    
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
    
    def buffer(self,*args,**kwargs):
        return self.unary_operation('buffer',*args,**kwargs)

    def dilate(self,*args,**kwargs):
        return self.unary_operation('dilate',*args,**kwargs)

    def erode(self,*args,**kwargs):
        return self.unary_operation('erode',*args,**kwargs)

    def translate(self,*args,**kwargs):
        return self.unary_operation('translate',*args,**kwargs)
        
    def rotate(self,*args,**kwargs):
        return self.unary_operation('rotate',*args,**kwargs)

    def affine_transform(self,*args,**kwargs):
        return self.unary_operation('affine_transform',*args,**kwargs)

    def map_line_stretch(self,*args,**kwargs):
        import math
        translate,rotate,scale = geometry.map_line(*args,**kwargs)
        laminate = self.affine_transform([scale,0,0,1,0,0])
        laminate = laminate.rotate(rotate*180/math.pi,origin=(0,0))
        laminate = laminate.translate(*translate)
        return laminate
        
    def export_dxf(self,name):
        for ii,layer in enumerate(self.layers):
            layername = name+str(ii)
            layer.export_dxf(layername)