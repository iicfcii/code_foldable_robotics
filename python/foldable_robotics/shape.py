# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes and CONTRIBUTORS
Email: danaukes<at>asu.edu.
Please see LICENSE for full license.
"""

import matplotlib.pyplot as plt
import numpy
from .class_algebra import ClassAlgebra
import shapely.geometry

class GeometryNotHandled(Exception):
    pass

def is_collection(item):
    collections = [
        shapely.geometry.MultiPolygon,
        shapely.geometry.GeometryCollection,
        shapely.geometry.MultiLineString,
        shapely.geometry.multilinestring.MultiLineString,
        shapely.geometry.MultiPoint]
    iscollection = [isinstance(item, cls) for cls in collections]
    return any(iscollection)
    
def extract_r(item,list_in = None):
    list_in = list_in or []
    if is_collection(item):
        list_in.extend([item3 for item2 in item.geoms for item3 in extract_r(item2,list_in)])
    else:
        list_in.append(item)
    return list_in
    
def condition_shapely_entities(*entities):
    entities = [item for item2 in entities for item in extract_r(item2)]
    entities = [item for item in entities if any([isinstance(item,classitem) for classitem in [shapely.geometry.Polygon,shapely.geometry.LineString,shapely.geometry.Point]])]
    entities = [item for item in entities if not item.is_empty]
#    entities = [item for item in entities if not item.is_valid]
    return entities

def unary_union_safe(*listin):
    '''try to perform a unary union.  if that fails, fall back to iterative union'''
    import shapely
    import shapely.ops as so

    try:
        return so.unary_union(listin)
    except (shapely.geos.TopologicalError, ValueError):
        print('Unary Union Failed.  Falling Back...')
        workinglist = listin[:]
        try:
            result = workinglist.pop(0)
            for item in workinglist:
                try:
                    newresult = result.union(item)
                    result = newresult
                except (shapely.geos.TopologicalError, ValueError):
                    raise
            return result
        except IndexError:
            raise

class Base(ClassAlgebra):
    resolution = 1
    circle_resolution = 8
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
        a = unary_union_safe(*csg_items)
        b = Base.from_shapely(a)
        return b
        
    def translate(self,dx,dy):
        exterior = (numpy.array(self.exterior)+numpy.array([dx,dy])).tolist()      
        interiors = [(numpy.array(interior)+numpy.array([dx,dy])).tolist() for interior in self.interiors]        
        new = type(self)(exterior,interiors)
        return new

    def R(self,t):
        import numpy
        from math import sin,cos
        cost = cos(t)
        sint = sin(t)
        R = numpy.array([[cost,-sint],[sint,cost]])
        return R
    
    def rotate(self,angle,about=None):
        from math import pi
        t = pi*angle/180
        R = self.R(t)
        
        if about is not None:
            self = self.translate(-about[0],-about[1])
        exterior = (R.dot(numpy.array(self.exterior).T)).T.tolist()
        interiors = [(R.dot(numpy.array(interior).T)).T.tolist() for interior in self.interiors]            
        new = type(self)(exterior,interiors)
        if about is not None:
            new = new.translate(about[0],about[1])
        return new

    @staticmethod
    def from_shapely(entity,outputlist=None):
        from .shape import Polygon,Polyline,Point
    
        entities = condition_shapely_entities(entity)

        outputlist = outputlist or []
        for entity in entities:
            if isinstance(entity, shapely.geometry.Polygon):
                outputlist.append(Polygon._from_shapely(entity))    
            elif isinstance(entity, shapely.geometry.LineString):
                outputlist.append(Polyline._from_shapely(entity))    
            elif isinstance(entity, shapely.geometry.Point):
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

    @classmethod    
    def make_rect_bl(cls,bottom_left,width,height):
        bl = numpy.array(bottom_left)
        exterior = numpy.array([bl,bl+[0,height],bl+[width,height],bl+[width,0]])
        return cls(exterior.tolist(),[])

    @classmethod    
    def make_rect_center(cls,width,height):
        center = numpy.array([0,0])
        exterior = numpy.array([center+[-width/2,-height/2],center+[-width/2,height/2],center+[width/2,height/2],center+[width/2,-height/2],])
        return cls(exterior.tolist(),[])

    @classmethod    
    def make_circle_r(cls,center,radius,resolution = None):
        resolution = resolution or cls.circle_resolution
        p = Point([center],[])
        new = p.dilate(radius,resolution)[0]
        return new
        
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