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

class GeometryNotHandled(Exception):
    pass

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
        return self.from_shapely(c)

    def difference(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.difference(b)
        return self.from_shapely(c)

    def intersection(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.intersection(b)
        return self.from_shapely(c)
        
    def symmetric_difference(self,other):
        a = self.to_shapely()
        b = other.to_shapely()
        c = a.symmetric_difference(b)
        return self.from_shapely(c)
    
    def dilate(self,value,resolution = None):
        resolution = resolution or self.resolution
        a = self.to_shapely()
        b = a.buffer(value,resolution = resolution)
        return self.from_shapely(b)

    def erode(self,value,resolution = None):
        resolution = resolution or self.resolution
        a = self.to_shapely()
        b = a.buffer(-value,resolution = resolution)
        return self.from_shapely(b)

    @staticmethod    
    def unary_union(*items):
        csg_items = [item.to_shapely() for item in items]        
        a = csg_shapely.unary_union_safe(*csg_items)
        b = Base.from_shapely(a)
        return b
        
    def shift(self,dx,dy):
        exterior = (numpy.array(self.exterior)+numpy.array([dx,dy])).tolist()      
        interiors = [(numpy.array(interior)+numpy.array([dx,dy])).tolist() for interior in self.interiors]        
        new = type(self)(exterior,interiors)
        return new

    @staticmethod
    def from_shapely(entity,outputlist=None):
        import shapely.geometry as sg
        from .shape import Polygon,Polyline,Point
    
        entities = csg_shapely.condition_shapely_entities(entity)

        outputlist = outputlist or []
        for entity in entities:
            if isinstance(entity, sg.Polygon):
                outputlist.append(Polygon._from_shapely(entity))    
            elif isinstance(entity, sg.LineString):
                outputlist.append(Polyline._from_shapely(entity))    
            elif isinstance(entity, sg.Point):
                outputlist.append(Point._from_shapely(entity))    
            else:
                raise GeometryNotHandled()
        return outputlist

        
class Polygon(Base):
    def to_shapely(self):
        obj = shapely.geometry.Polygon(self.exterior, self.interiors)
        return obj
        
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
        patch = PathPatch(path,facecolor=(1,0,0,.25),edgecolor=(1,0,0,.5))        
        axes.add_patch(patch)
        plt.axis('equal')

    @classmethod
    def _from_shapely(cls,entity):
        exterior = [coord for coord in entity.exterior.coords]        
        interiors = [[coord for coord in interior.coords] for interior in entity.interiors]
        return cls(exterior, interiors)
        
class Polyline(Base):
    def to_shapely(self):
        obj = shapely.geometry.LineString(self.exterior)
        return obj

    def plot(self):
        plt.plot(*numpy.array(self.exterior).T,color=(0,1,0,.5),linewidth=2)
#        [plt.plot(*numpy.array(interior).T) for interior in self.interiors]
        plt.axis('equal')

    @classmethod
    def _from_shapely(cls,entity):
        exterior = [coord for coord in entity.coords]        
        return cls(exterior, [])

class Point(Base):
    def to_shapely(self):
        obj = shapely.geometry.Point(*self.exterior[0])
        return obj
    def plot(self):
        plt.plot(*numpy.array(self.exterior).T,marker = 'o',color=(0,0,1,.5))
#        [plt.plot(*numpy.array(interior).T) for interior in self.interiors]
        plt.axis('equal')
    @classmethod
    def _from_shapely(cls,entity):
        exterior = [coord for coord in entity.coords]        
        return cls(exterior, [])        
if __name__=='__main__':
  pass