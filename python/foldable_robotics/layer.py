# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
#import shapely.geometry as sg
from .shape import Base
from . import shape
from .class_algebra import ClassAlgebra
import matplotlib.pyplot as plt

class Layer(ClassAlgebra):

    def __init__(self, *geoms):
        geoms = self.flatten(geoms)
        self.geoms = geoms
        self.id = id(self)

    @classmethod
    def new(cls,*geoms):
        geoms = cls.flatten(geoms)
        new = cls(*geoms)
        return new

    def copy(self,identical = True):
        new = type(self)(*[geom.copy(identical) for geom in self.geoms])        
        if identical:        
            new.id = self.id
        return new

    def plot(self,*args,**kwargs):
        if 'new' in kwargs:
            new = kwargs.pop('new')
        else:
            new = False
        if new:
            plt.figure()
        for geom in self.geoms:
            geom.plot(*args,**kwargs)

    def binary_operation(self,other,function_name):
        a = shape.unary_union_safe(*[item.to_shapely() for item in self.geoms])
        b = shape.unary_union_safe(*[item.to_shapely() for item in other.geoms])
        function = getattr(a,function_name)
        c = function(b)
        d = Base.from_shapely(c)
        e = self.flatten(d)
        return type(self)(*e)

    @staticmethod
    def flatten(geoms):
        return Base.unary_union(*geoms)

    def union(self,other):
        return self.binary_operation(other,'union')

    def difference(self,other):
        return self.binary_operation(other,'difference')

    def symmetric_difference(self,other):
        return self.binary_operation(other,'symmetric_difference')

    def intersection(self,other):
        return self.binary_operation(other,'intersection')
    
    def dilate(self,value,resolution = None):
        new_geoms = [item for geom in self.geoms for item in geom.dilate(value,resolution)]
        new_geoms = self.flatten(new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def erode(self,value,resolution = None):
        new_geoms = [item for geom in self.geoms for item in geom.dilate(-value,resolution)]
        new_geoms = self.flatten(new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def translate(self,dx,dy):
        new_geoms = [geom.translate(dx,dy) for geom in self.geoms]
        new_layer = type(self)(*new_geoms)
        return new_layer

    def rotate(self,angle,about=None):
        new_geoms = [geom.rotate(angle,about) for geom in self.geoms]
        new_layer = type(self)(*new_geoms)
        return new_layer
        