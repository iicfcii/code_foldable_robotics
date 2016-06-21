# -*- coding: utf-8 -*-
"""
Created on Mon May 16 09:55:55 2016

@author: danb0b
"""
import csg_shapely

class ClassAlgebra(object):

    def __or__(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.union(b)
        return csg_shapely.to_generic(c)
        
    def __sub__(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.difference(b)
        return csg_shapely.to_generic(c)
    
    def __and__(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.intersection(b)
        return csg_shapely.to_generic(c)
        
    def __xor__(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.symmetric_difference(b)
        return csg_shapely.to_generic(c)        