# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

#import shapely.geometry as sg
#from . import genericshapebase
import matplotlib.pyplot as plt
import numpy
#from . import shapely_algebra 
from . import csg_shapely
from .class_algebra import ClassAlgebra
import shapely.geometry

class Base(ClassAlgebra):
    resolution = 1
    
    def __init__(self,exterior,interiors):
        self.id = id(self)
        self.exterior = exterior
        self.interiors = interiors
       
    def copy_data(self,new_class, identical):
        new = new_class(self.exterior.copy(),[interior.copy for interior in self.interiors])        
        if identical:        
            new.id = self.id
        return new

    def copy(self,identical = True):
        return self.copy_data(type(self))
    
    def copy_into_me(self,other):
        self.exterior = other.get_exterior.copy()
        self.interiors = [item.copy() for item in other.get_interiors()]
        self.construction = other.is_construction()

    def segments(self):
        return self.segments_closed()
        
    def closepath(self,list_in):
        out = list_in[1:]+list_in[0:1]
        return out

    def union(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.union(b)
        return csg_shapely.to_generic(c)

    def difference(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.difference(b)
        return csg_shapely.to_generic(c)

    def intersection(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.intersection(b)
        return csg_shapely.to_generic(c)
        
    def symmetric_difference(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.symmetric_difference(b)
        return csg_shapely.to_generic(c)        
    
    def dilate(self,value,resolution = None):
        resolution = resolution or self.resolution
        a = self.to_shapely()
        b = a.buffer(value,resolution = resolution)
        return csg_shapely.to_generic(b)

    def erode(self,value,resolution = None):
        resolution = resolution or self.resolution
        a = self.to_shapely()
        b = a.buffer(-value,resolution = resolution)
        return csg_shapely.to_generic(b)

    @staticmethod    
    def unary_union(*items):
        csg_items = [item.to_shapely() for item in items]        
        a = csg_shapely.unary_union_safe(*csg_items)
        b = csg_shapely.to_generic(a)
        return b
        
    def shift(self,dx,dy):
        exterior = numpy.array(self.exterior)+numpy.array([dx,dy]).tolist()      
        interiors = [numpy.array(interior)+numpy.array([dx,dy]).tolist() for interior in self.interiors]        
        new = type(self)(exterior,interiors)
        return new
        
class Polygon(Base):
    def to_shapely(self):
        obj = shapely.geometry.Polygon(self.exterior, self.interiors)
        return obj
#    def plot(self):
#        plt.fill(*numpy.array(self.exterior).T,color=(1,0,0,.25))
#        ext = numpy.array(self.exterior)
#        ints =[numpy.array(interior) for interior in self.interiors]
#        plt.plot(*self.closepath(ext).T)
#        [plt.plot(*self.closepath(interior).T) for interior in ints]
#        plt.axis('equal')
        
    def plot(self):
        from matplotlib.patches import PathPatch
        from matplotlib.path import Path
        axes = plt.gca()
        vertices = []
        codes = []
        for item in [self.exterior]+self.interiors:
            vertices.extend(item+[(0,0)])
            codes.extend([Path.MOVETO]+([Path.LINETO]*(len(item)-1))+[Path.CLOSEPOLY])
        path = Path(vertices,codes)
        patch = PathPatch(path,color=(1,0,0,.25))        
        axes.add_patch(patch)
        plt.axis('equal')

class Polyline(Base):
    def to_shapely(self):
        obj = shapely.geometry.LineString(self.exterior)
        return obj
    def plot(self):
        plt.plot(*numpy.array(self.exterior).T,color=(0,1,0,.5))
#        [plt.plot(*numpy.array(interior).T) for interior in self.interiors]
        plt.axis('equal')
        
if __name__=='__main__':
  pass