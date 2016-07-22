# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""
#import shapely.geometry as sg
from . import csg_shapely
from .shape import Base
from .class_algebra import ClassAlgebra

class Layer(ClassAlgebra):

    def __init__(self, *geoms):
        self.geoms = geoms
        self.id = id(self)

    @classmethod
    def new(cls,*geoms):
        geoms = Base.unary_union(*geoms)
        new = cls(*geoms)
        return new

    def copy(self,identical = True):
        new = type(self)(*[geom.copy(identical) for geom in self.geoms])        
        if identical:        
            new.id = self.id
        return new

    def plot(self):
        for geom in self.geoms:
            geom.plot()

    def unary_operation(self,other,function_name):
        a = csg_shapely.unary_union_safe(*[item.to_shapely() for item in self.geoms])
        b = csg_shapely.unary_union_safe(*[item.to_shapely() for item in other.geoms])
        function = getattr(a,function_name)
        c = function(b)
        e = Base.from_shapely(c)
        return type(self)(*e)

    def union(self,other):
        return self.unary_operation(other,'union')

    def intersection(self,other):
        return self.unary_operation(other,'intersection')
    
    def translate(self,dx,dy):
        new_geoms = [geom.translate(dx,dy) for geom in self.geoms]
        new_layer = type(self)(*new_geoms)
        return new_layer

    def rotate(self,angle,about=None):
        new_geoms = [geom.rotate(angle,about) for geom in self.geoms]
        new_layer = type(self)(*new_geoms)
        return new_layer

    def dilate(self,value,resolution = None):
        new_geoms = [geom.dilate(value,resolution)[0] for geom in self.geoms]
        new_geoms = Base.unary_union(*new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer

    def difference(self,other):
        new_geoms = []
        for item1 in self.geoms:
            result = [item1]
            for item2 in other.geoms:
                result = [item3 for item in result for item3 in item-item2 ]
            new_geoms.extend(result)                
        new_geoms = Base.unary_union(*new_geoms)        
        new_layer = type(self)(*new_geoms)
        return new_layer
        